class Calculator:
    def multiply(self, val1, val2) -> float:
        return float(val1) * float(val2)
        
    def calculate_total(self, *costs) -> float:
        return sum(float(c) for c in costs)
        
    def calculate_daily_budget(self, total_cost: float, days: int) -> float:
        if days <= 0:
            return float(total_cost)
        return float(total_cost) / float(days)