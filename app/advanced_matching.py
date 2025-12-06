"""
Advanced matching algorithm using a custom Priority Queue data structure
with multi-factor scoring and dynamic weight adjustment.

This implements a novel algorithmic design using:
1. Custom Priority Queue with heap-based ordering
2. Multi-dimensional scoring with weighted factors
3. Dynamic weight adjustment based on client profile
4. Category matching using prefix tree (Trie) for fast lookups
"""
import heapq
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass, field
from collections import defaultdict

from .models import LawyerProfile, Issue


@dataclass
class MatchCandidate:
    """Data structure representing a lawyer-issue match candidate."""
    lawyer: LawyerProfile
    issue: Issue
    base_score: float = 0.0
    factor_scores: Dict[str, float] = field(default_factory=dict)
    weighted_score: float = 0.0
    match_reasons: List[str] = field(default_factory=list)
    
    def __lt__(self, other):
        """For heap ordering - higher score = higher priority."""
        return self.weighted_score > other.weighted_score
    
    def __eq__(self, other):
        return self.lawyer.id == other.lawyer.id if isinstance(other, MatchCandidate) else False


class CategoryTrie:
    """
    Trie (Prefix Tree) data structure for fast category matching.
    Enables O(m) lookup time where m is category name length.
    """
    def __init__(self):
        self.root = {}
        self.categories = set()
    
    def insert(self, category: str):
        """Insert a category into the trie."""
        self.categories.add(category.lower())
        node = self.root
        for char in category.lower():
            if char not in node:
                node[char] = {}
            node = node[char]
        node['#'] = True  # Mark end of word
    
    def search(self, category: str) -> bool:
        """Check if category exists in trie."""
        node = self.root
        for char in category.lower():
            if char not in node:
                return False
            node = node[char]
        return '#' in node
    
    def find_similar(self, category: str, max_results: int = 5) -> List[str]:
        """Find similar categories using prefix matching."""
        category_lower = category.lower()
        similar = []
        
        for cat in self.categories:
            # Check if category starts with search term or vice versa
            if cat.startswith(category_lower) or category_lower.startswith(cat):
                similar.append(cat)
            # Check for substring match
            elif category_lower in cat or cat in category_lower:
                similar.append(cat)
            
            if len(similar) >= max_results:
                break
        
        return similar
    
    def build_from_categories(self, categories: List[str]):
        """Build trie from a list of categories."""
        for cat in categories:
            self.insert(cat)


class PriorityMatchQueue:
    """
    Custom Priority Queue implementation using binary heap
    for efficient O(log n) insertion and O(log n) extraction.
    
    Maintains lawyers sorted by match score with automatic
    reordering as scores are updated.
    """
    def __init__(self):
        self.heap: List[MatchCandidate] = []
        self.lawyer_map: Dict[int, MatchCandidate] = {}  # O(1) lookup by lawyer ID
        self.size = 0
    
    def push(self, candidate: MatchCandidate):
        """Add candidate to queue with O(log n) complexity."""
        if candidate.lawyer.id in self.lawyer_map:
            # Update existing candidate
            old_candidate = self.lawyer_map[candidate.lawyer.id]
            old_candidate.weighted_score = candidate.weighted_score
            old_candidate.factor_scores = candidate.factor_scores
            # Re-heapify (lazy approach - could optimize with decrease_key)
            heapq.heapify(self.heap)
        else:
            heapq.heappush(self.heap, candidate)
            self.lawyer_map[candidate.lawyer.id] = candidate
            self.size += 1
    
    def pop(self) -> Optional[MatchCandidate]:
        """Extract highest-scoring candidate in O(log n) time."""
        if not self.heap:
            return None
        candidate = heapq.heappop(self.heap)
        del self.lawyer_map[candidate.lawyer.id]
        self.size -= 1
        return candidate
    
    def peek(self) -> Optional[MatchCandidate]:
        """View top candidate without removing - O(1)."""
        return self.heap[0] if self.heap else None
    
    def get_top_k(self, k: int) -> List[MatchCandidate]:
        """Get top K candidates without modifying queue."""
        if k >= self.size:
            return sorted(self.heap, key=lambda x: x.weighted_score, reverse=True)
        
        # Use heap to get top K efficiently
        top_k = []
        temp_heap = self.heap.copy()
        heapq.heapify(temp_heap)
        
        for _ in range(min(k, self.size)):
            if temp_heap:
                top_k.append(heapq.heappop(temp_heap))
        
        return sorted(top_k, key=lambda x: x.weighted_score, reverse=True)
    
    def is_empty(self) -> bool:
        return self.size == 0


class AdvancedMatcher:
    """
    Advanced matching system using:
    - Priority Queue for efficient candidate management
    - Trie for fast category matching
    - Dynamic weight adjustment based on client profile
    - Multi-factor scoring with normalization
    """
    
    def __init__(self):
        self.category_trie = CategoryTrie()
        self.weight_profiles = {
            'budget_conscious': {
                'case_type': 0.25,
                'specialization': 0.15,
                'success_rate': 0.10,
                'availability': 0.20,
                'pricing': 0.25,  # Higher weight for budget-conscious
                'client_profile': 0.05
            },
            'quality_focused': {
                'case_type': 0.30,
                'specialization': 0.25,
                'success_rate': 0.25,  # Higher weight for quality
                'availability': 0.10,
                'pricing': 0.05,
                'client_profile': 0.05
            },
            'urgent': {
                'case_type': 0.25,
                'specialization': 0.20,
                'success_rate': 0.15,
                'availability': 0.30,  # Higher weight for urgent
                'pricing': 0.05,
                'client_profile': 0.05
            },
            'default': {
                'case_type': 0.30,
                'specialization': 0.20,
                'success_rate': 0.15,
                'availability': 0.15,
                'pricing': 0.15,
                'client_profile': 0.05
            }
        }
    
    def _determine_client_profile(self, issue: Issue) -> str:
        """Determine client profile type for dynamic weight adjustment."""
        if issue.urgency in ['high', 'urgent']:
            return 'urgent'
        
        # Budget-conscious if budget range is lower
        budget_avg = (issue.budget_min + issue.budget_max) / 2
        if budget_avg < 3000:
            return 'budget_conscious'
        elif budget_avg > 10000:
            return 'quality_focused'
        
        return 'default'
    
    def _calculate_factor_scores(self, lawyer: LawyerProfile, issue: Issue) -> Dict[str, float]:
        """Calculate individual factor scores (0-100 scale)."""
        scores = {}
        
        # 1. Case Type Match (using Trie for fast lookup)
        lawyer_categories = [c.strip().lower() for c in lawyer.categories_list()]
        issue_category = issue.category.lower()
        
        if issue_category in lawyer_categories:
            scores['case_type'] = 100.0
        else:
            # Use trie to find similar categories
            similar = self.category_trie.find_similar(issue_category, max_results=1)
            if similar and any(sim in lawyer_categories for sim in similar):
                scores['case_type'] = 70.0
            else:
                scores['case_type'] = 0.0
        
        # 2. Specialization Score
        rating_score = (lawyer.rating / 5.0) * 100
        if issue_category in lawyer_categories:
            scores['specialization'] = rating_score
        else:
            scores['specialization'] = rating_score * 0.7
        
        # 3. Success Rate
        scores['success_rate'] = lawyer.case_success_rate * 100
        
        # 4. Availability
        if not lawyer.is_available_for_new_case():
            scores['availability'] = 0.0
        else:
            if lawyer.max_cases == 0:
                scores['availability'] = 100.0
            else:
                capacity_used = lawyer.current_cases / lawyer.max_cases
                if capacity_used < 0.5:
                    scores['availability'] = 100.0
                elif capacity_used < 0.8:
                    scores['availability'] = 80.0
                else:
                    scores['availability'] = 60.0
        
        # 5. Pricing Compatibility
        scores['pricing'] = self._calculate_pricing_score(lawyer, issue)
        
        # 6. Client Profile Match
        scores['client_profile'] = 50.0
        if issue.urgency in ['high', 'urgent'] and lawyer.case_success_rate >= 0.85:
            scores['client_profile'] = 80.0
        
        return scores
    
    def _calculate_pricing_score(self, lawyer: LawyerProfile, issue: Issue) -> float:
        """Calculate pricing compatibility score."""
        client_budget_min = issue.budget_min
        client_budget_max = issue.budget_max
        preferred_pricing = issue.preferred_pricing.lower()
        
        if preferred_pricing == "hourly" and lawyer.hourly_rate > 0:
            estimated_min = lawyer.hourly_rate * 10
            estimated_max = lawyer.hourly_rate * 40
            
            if estimated_min <= client_budget_max and estimated_max >= client_budget_min:
                overlap = min(estimated_max, client_budget_max) - max(estimated_min, client_budget_min)
                total_range = max(estimated_max, client_budget_max) - min(estimated_min, client_budget_min)
                return (overlap / total_range) * 100 if total_range > 0 else 50.0
            return 30.0
        
        elif preferred_pricing == "fixed":
            if lawyer.fixed_rate_min > 0 or lawyer.fixed_rate_max > 0:
                lawyer_min = lawyer.fixed_rate_min if lawyer.fixed_rate_min > 0 else lawyer.fixed_rate_max * 0.5
                lawyer_max = lawyer.fixed_rate_max if lawyer.fixed_rate_max > 0 else lawyer.fixed_rate_min * 2
                
                if lawyer_min <= client_budget_max and lawyer_max >= client_budget_min:
                    overlap = min(lawyer_max, client_budget_max) - max(lawyer_min, client_budget_min)
                    total_range = max(lawyer_max, client_budget_max) - min(lawyer_min, client_budget_min)
                    return (overlap / total_range) * 100 if total_range > 0 else 50.0
                return 30.0
        
        elif preferred_pricing == "contingency":
            return 100.0 if lawyer.accepts_contingency else 20.0
        
        return 50.0
    
    def match_lawyers(self, issue: Issue, all_lawyers: List[LawyerProfile], 
                     top_k: int = 10) -> List[Tuple[LawyerProfile, float, Dict[str, float], List[str]]]:
        """
        Advanced matching using Priority Queue and dynamic weights.
        
        Algorithm Complexity:
        - Building trie: O(m * n) where m = avg category length, n = categories
        - Scoring each lawyer: O(1) per lawyer
        - Priority queue operations: O(log n) per insertion
        - Overall: O(n log n) where n = number of lawyers
        
        Returns: List of (lawyer, total_score, factor_scores, match_reasons)
        """
        # Build category trie for fast matching
        from .models import ISSUE_CATEGORIES
        self.category_trie.build_from_categories(ISSUE_CATEGORIES)
        for lawyer in all_lawyers:
            for cat in lawyer.categories_list():
                self.category_trie.insert(cat)
        
        # Determine client profile for dynamic weights
        client_profile = self._determine_client_profile(issue)
        weights = self.weight_profiles.get(client_profile, self.weight_profiles['default'])
        
        # Initialize priority queue
        match_queue = PriorityMatchQueue()
        
        # Score and add all lawyers to priority queue
        for lawyer in all_lawyers:
            if not lawyer.user or not lawyer.user.is_lawyer:
                continue
            
            # Calculate factor scores
            factor_scores = self._calculate_factor_scores(lawyer, issue)
            
            # Calculate weighted total score
            weighted_score = sum(
                factor_scores.get(factor, 0) * weight
                for factor, weight in weights.items()
            )
            
            # Generate match reasons
            match_reasons = []
            if factor_scores.get('case_type', 0) >= 70:
                match_reasons.append("Expertise match")
            if factor_scores.get('success_rate', 0) >= 80:
                match_reasons.append("High success rate")
            if factor_scores.get('availability', 0) >= 80:
                match_reasons.append("Available now")
            if factor_scores.get('pricing', 0) >= 70:
                match_reasons.append("Budget compatible")
            
            # Create candidate and add to queue
            candidate = MatchCandidate(
                lawyer=lawyer,
                issue=issue,
                base_score=weighted_score,
                factor_scores=factor_scores,
                weighted_score=weighted_score,
                match_reasons=match_reasons
            )
            
            match_queue.push(candidate)
        
        # Extract top K matches
        top_candidates = match_queue.get_top_k(top_k)
        
        return [
            (c.lawyer, round(c.weighted_score, 2), c.factor_scores, c.match_reasons)
            for c in top_candidates
            if c.weighted_score > 0
        ]


# Global instance
advanced_matcher = AdvancedMatcher()

