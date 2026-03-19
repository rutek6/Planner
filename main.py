import classes
import parser
import plan

parsedPlan = parsePlan()
allCombinations = plan.dfs(parsedPlan)