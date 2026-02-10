// Cognitive Architecture - Reasoning Engine Component
// Advanced logical reasoning for AI agents

class ReasoningEngine {
  constructor(memorySystem) {
    this.memory = memorySystem;
    this.rules = [];
    this.facts = [];
  }

  // Add a rule to the knowledge base
  addRule(condition, action, priority = 1) {
    const rule = {
      id: `rule_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      condition,
      action,
      priority,
      createdAt: new Date().toISOString()
    };
    
    this.rules.push(rule);
    return rule.id;
  }

  // Add a fact to the knowledge base
  addFact(subject, predicate, object, confidence = 1.0) {
    const fact = {
      id: `fact_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      subject,
      predicate,
      object,
      confidence,
      createdAt: new Date().toISOString()
    };
    
    this.facts.push(fact);
    return fact.id;
  }

  // Deductive reasoning: derive specific conclusions from general rules
  deduct(knownFacts = null) {
    const factsToUse = knownFacts || this.facts;
    const conclusions = [];
    
    // Sort rules by priority (higher first)
    const sortedRules = [...this.rules].sort((a, b) => b.priority - a.priority);
    
    for (const rule of sortedRules) {
      try {
        // Check if rule's condition is satisfied by known facts
        const matchedFacts = this.matchConditionToFacts(rule.condition, factsToUse);
        if (matchedFacts.length > 0) {
          // Apply rule's action to generate conclusion
          const conclusion = this.applyAction(rule.action, matchedFacts);
          conclusions.push({
            sourceRule: rule.id,
            conclusion,
            confidence: Math.min(...matchedFacts.map(f => f.confidence)),
            timestamp: new Date().toISOString()
          });
        }
      } catch (error) {
        console.warn(`Error applying rule ${rule.id}:`, error.message);
      }
    }
    
    return conclusions;
  }

  // Match a condition against known facts
  matchConditionToFacts(condition, facts) {
    const matches = [];
    
    for (const fact of facts) {
      let isMatch = true;
      
      // Simple pattern matching - in reality this would be more sophisticated
      if (condition.subject && fact.subject !== condition.subject) isMatch = false;
      if (condition.predicate && fact.predicate !== condition.predicate) isMatch = false;
      if (condition.object && fact.object !== condition.object) isMatch = false;
      
      if (isMatch) {
        matches.push(fact);
      }
    }
    
    return matches;
  }

  // Apply an action to generate a conclusion
  applyAction(action, matchedFacts) {
    // This is a simplified implementation
    // Real implementation would depend on the action type
    if (typeof action === 'function') {
      return action(matchedFacts);
    } else if (typeof action === 'object') {
      return { ...action, derivedFrom: matchedFacts.map(f => f.id) };
    }
    
    return action;
  }

  // Inductive reasoning: derive general rules from specific observations
  induct(observations, minConfidence = 0.7) {
    // Group observations by patterns
    const patterns = {};
    
    for (const obs of observations) {
      const key = this.generatePatternKey(obs);
      if (!patterns[key]) patterns[key] = [];
      patterns[key].push(obs);
    }
    
    const hypotheses = [];
    
    for (const [pattern, obsList] of Object.entries(patterns)) {
      if (obsList.length >= 2) { // Require at least 2 observations for a pattern
        const confidence = obsList.length / observations.length;
        
        if (confidence >= minConfidence) {
          const hypothesis = this.formulateHypothesis(obsList, confidence);
          hypotheses.push(hypothesis);
        }
      }
    }
    
    return hypotheses;
  }

  // Generate a pattern key for grouping similar observations
  generatePatternKey(observation) {
    // Create a hashable key based on observation properties
    const keys = Object.keys(observation).sort();
    return keys.map(k => `${k}:${observation[k]}`).join('|');
  }

  // Formulate a hypothesis from a set of observations
  formulateHypothesis(observations, confidence) {
    // Extract common patterns from observations
    const commonProps = {};
    
    // Find properties that are consistent across observations
    if (observations.length > 0) {
      const firstObs = observations[0];
      for (const [key, value] of Object.entries(firstObs)) {
        const isConsistent = observations.every(obs => obs[key] === value);
        if (isConsistent) {
          commonProps[key] = value;
        }
      }
    }
    
    return {
      type: 'inductive_hypothesis',
      pattern: commonProps,
      observations: observations.length,
      confidence,
      timestamp: new Date().toISOString()
    };
  }

  // Abductive reasoning: find best explanation for observations
  abduct(observations, possibleExplanations, selectionCriteria = 'simplicity') {
    let bestExplanation = null;
    let bestScore = -Infinity;
    
    for (const explanation of possibleExplanations) {
      const score = this.evaluateExplanation(explanation, observations, selectionCriteria);
      if (score > bestScore) {
        bestScore = score;
        bestExplanation = explanation;
      }
    }
    
    return {
      explanation: bestExplanation,
      score: bestScore,
      criteria: selectionCriteria,
      timestamp: new Date().toISOString()
    };
  }

  // Evaluate how well an explanation fits observations
  evaluateExplanation(explanation, observations, criteria) {
    let score = 0;
    
    switch (criteria) {
      case 'completeness': // How many observations does it explain?
        score = this.evaluateCompleteness(explanation, observations);
        break;
      case 'consistency': // How consistent is it with known facts?
        score = this.evaluateConsistency(explanation, observations);
        break;
      case 'simplicity': // How simple is the explanation?
        score = this.evaluateSimplicity(explanation);
        break;
      default:
        // Weighted combination
        const completeness = this.evaluateCompleteness(explanation, observations);
        const consistency = this.evaluateConsistency(explanation, observations);
        const simplicity = this.evaluateSimplicity(explanation);
        score = (completeness * 0.4) + (consistency * 0.4) + (simplicity * 0.2);
    }
    
    return score;
  }

  // Evaluate completeness of an explanation
  evaluateCompleteness(explanation, observations) {
    // For now, return a simple ratio of explained observations
    return 0.7; // Placeholder - would be more sophisticated in practice
  }

  // Evaluate consistency of an explanation
  evaluateConsistency(explanation, observations) {
    // Check if explanation is consistent with known facts
    return 0.8; // Placeholder - would be more sophisticated in practice
  }

  // Evaluate simplicity of an explanation
  evaluateSimplicity(explanation) {
    // Simpler explanations get higher scores
    const complexity = JSON.stringify(explanation).length;
    return 1 / (1 + complexity / 100); // Normalize to 0-1 range
  }

  // Problem solving using means-end analysis
  solveProblem(initialState, goalState, operators, maxIterations = 100) {
    // Breadth-First Search approach to problem solving
    const queue = [{ 
      state: this.cloneState(initialState), 
      path: [],
      cost: 0,
      depth: 0
    }];
    
    const visited = new Set([this.stateToString(initialState)]);
    let iterations = 0;
    
    while (queue.length > 0 && iterations < maxIterations) {
      iterations++;
      const { state, path, cost, depth } = queue.shift();
      
      // Check if goal reached
      if (this.isGoalReached(state, goalState)) {
        return {
          solution: path,
          cost,
          depth,
          iterations,
          success: true
        };
      }
      
      // Apply all applicable operators
      for (const op of operators) {
        if (this.isOperatorApplicable(state, op)) {
          const newState = this.applyOperator(state, op);
          const stateKey = this.stateToString(newState);
          
          if (!visited.has(stateKey)) {
            visited.add(stateKey);
            queue.push({
              state: newState,
              path: [...path, { operator: op.name, description: op.description }],
              cost: cost + (op.cost || 1),
              depth: depth + 1
            });
          }
        }
      }
    }
    
    return {
      solution: null,
      iterations,
      success: false,
      message: 'No solution found within iteration limit'
    };
  }

  // Clone state to avoid mutation
  cloneState(state) {
    return JSON.parse(JSON.stringify(state));
  }

  // Convert state to string for visited set
  stateToString(state) {
    return JSON.stringify(state, Object.keys(state).sort());
  }

  // Check if goal state is reached
  isGoalReached(state, goalState) {
    return Object.keys(goalState).every(key => 
      state[key] !== undefined && state[key] === goalState[key]
    );
  }

  // Check if operator is applicable to current state
  isOperatorApplicable(state, operator) {
    if (!operator.preconditions) return true;
    
    return operator.preconditions.every(condition => {
      const { attribute, value, comparison } = condition;
      const currentValue = state[attribute];
      
      switch (comparison) {
        case 'equals': return currentValue === value;
        case 'greater_than': return currentValue > value;
        case 'less_than': return currentValue < value;
        case 'contains': return Array.isArray(currentValue) && currentValue.includes(value);
        default: return currentValue === value;
      }
    });
  }

  // Apply operator to state
  applyOperator(state, operator) {
    const newState = { ...state };
    
    if (operator.effects) {
      for (const effect of operator.effects) {
        const { attribute, value, operation } = effect;
        
        switch (operation) {
          case 'set':
            newState[attribute] = value;
            break;
          case 'add':
            if (typeof newState[attribute] === 'number') {
              newState[attribute] += value;
            } else if (Array.isArray(newState[attribute])) {
              newState[attribute] = [...newState[attribute], ...value];
            }
            break;
          case 'remove':
            if (Array.isArray(newState[attribute])) {
              newState[attribute] = newState[attribute].filter(item => !value.includes(item));
            } else {
              delete newState[attribute];
            }
            break;
          default:
            newState[attribute] = value;
        }
      }
    }
    
    return newState;
  }

  // Get reasoning engine statistics
  getStats() {
    return {
      rulesCount: this.rules.length,
      factsCount: this.facts.length,
      timestamp: new Date().toISOString()
    };
  }

  // Reset the reasoning engine
  reset() {
    this.rules = [];
    this.facts = [];
    return { success: true, message: 'Reasoning engine reset' };
  }
}

module.exports = ReasoningEngine;