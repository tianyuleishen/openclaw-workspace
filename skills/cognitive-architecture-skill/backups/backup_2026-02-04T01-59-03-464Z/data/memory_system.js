// Cognitive Architecture - Memory System Component
// Advanced memory management for AI agents

class MemorySystem {
  constructor(options = {}) {
    this.shortTermMemory = new Map();
    this.longTermMemory = new Map();
    this.episodicMemory = [];
    this.semanticMemory = new Map();
    this.proceduralMemory = new Map();
    this.options = {
      shortTermTTL: options.shortTermTTL || 300000, // 5 minutes default
      maxEpisodicSize: options.maxEpisodicSize || 1000,
      ...options
    };
  }

  // Store in short-term memory (volatile)
  storeShortTerm(key, data, ttl = this.options.shortTermTTL) {
    this.shortTermMemory.set(key, {
      data,
      timestamp: Date.now(),
      ttl
    });
    
    // Set cleanup timeout
    setTimeout(() => {
      if (this.shortTermMemory.has(key)) {
        const item = this.shortTermMemory.get(key);
        if (Date.now() >= item.timestamp + item.ttl) {
          this.shortTermMemory.delete(key);
        }
      }
    }, ttl);
    
    return { success: true, key, ttl };
  }

  // Store in long-term memory (persistent)
  storeLongTerm(key, data, category = 'general') {
    this.longTermMemory.set(key, {
      data,
      timestamp: new Date().toISOString(),
      category,
      accessed: 0,
      modified: new Date().toISOString()
    });
    
    return { success: true, key, category };
  }

  // Retrieve from memory with optional type restriction
  retrieve(key, memoryType = 'any') {
    if (memoryType === 'short' || memoryType === 'any') {
      const shortItem = this.shortTermMemory.get(key);
      if (shortItem && Date.now() < shortItem.timestamp + shortItem.ttl) {
        return { data: shortItem.data, type: 'short-term', key };
      } else if (shortItem) {
        this.shortTermMemory.delete(key); // Clean up expired
      }
    }

    if (memoryType === 'long' || memoryType === 'any') {
      const longItem = this.longTermMemory.get(key);
      if (longItem) {
        longItem.accessed += 1; // Track access count
        longItem.lastAccessed = new Date().toISOString();
        return { data: longItem.data, type: 'long-term', key, category: longItem.category };
      }
    }

    return null;
  }

  // Store episodic memory (sequence of events)
  storeEpisode(event, context = {}, timestamp = null) {
    const episode = {
      event,
      context,
      timestamp: timestamp || new Date().toISOString()
    };
    
    this.episodicMemory.push(episode);

    // Limit size to prevent memory bloat
    if (this.episodicMemory.length > this.options.maxEpisodicSize) {
      this.episodicMemory = this.episodicMemory.slice(-(this.options.maxEpisodicSize / 2)); // Keep last half
    }
    
    return { success: true, episodeCount: this.episodicMemory.length };
  }

  // Store semantic memory (facts and concepts)
  storeSemantic(concept, definition, relationships = [], metadata = {}) {
    this.semanticMemory.set(concept, {
      definition,
      relationships,
      metadata,
      lastUpdated: new Date().toISOString(),
      version: 1
    });
    
    return { success: true, concept };
  }

  // Store procedural memory (how-to knowledge)
  storeProcedure(name, steps, conditions = {}, metadata = {}) {
    this.proceduralMemory.set(name, {
      steps,
      conditions,
      metadata,
      lastUsed: new Date().toISOString(),
      usageCount: 0
    });
    
    return { success: true, procedure: name };
  }

  // Retrieve related concepts (semantic associations)
  findRelated(concept, maxResults = 5) {
    const conceptData = this.semanticMemory.get(concept);
    if (!conceptData) return [];

    // Return direct relationships
    return conceptData.relationships.slice(0, maxResults);
  }

  // Search for information across all memory types
  search(query, options = {}) {
    const results = [];
    
    // Search short-term memory
    if (!options.excludeShortTerm) {
      for (const [key, item] of this.shortTermMemory.entries()) {
        if (this.matchesQuery(item.data, query)) {
          results.push({
            key,
            data: item.data,
            type: 'short-term',
            relevance: this.calculateRelevance(item.data, query)
          });
        }
      }
    }

    // Search long-term memory
    if (!options.excludeLongTerm) {
      for (const [key, item] of this.longTermMemory.entries()) {
        if (this.matchesQuery(item.data, query)) {
          results.push({
            key,
            data: item.data,
            type: 'long-term',
            category: item.category,
            relevance: this.calculateRelevance(item.data, query)
          });
        }
      }
    }

    // Sort by relevance
    results.sort((a, b) => b.relevance - a.relevance);
    
    return results.slice(0, options.maxResults || 10);
  }

  // Helper method to match query against data
  matchesQuery(data, query) {
    if (typeof data === 'string') {
      return data.toLowerCase().includes(query.toLowerCase());
    } else if (typeof data === 'object') {
      const dataString = JSON.stringify(data).toLowerCase();
      return dataString.includes(query.toLowerCase());
    }
    return false;
  }

  // Calculate relevance score (simplified)
  calculateRelevance(data, query) {
    const dataString = typeof data === 'string' ? data : JSON.stringify(data);
    const lowerData = dataString.toLowerCase();
    const lowerQuery = query.toLowerCase();
    
    // Count occurrences of query terms
    const matches = (lowerData.match(new RegExp(lowerQuery, 'g')) || []).length;
    return matches;
  }

  // Get memory statistics
  getStats() {
    return {
      shortTerm: this.shortTermMemory.size,
      longTerm: this.longTermMemory.size,
      episodic: this.episodicMemory.length,
      semantic: this.semanticMemory.size,
      procedural: this.proceduralMemory.size,
      totalEstimatedSize: this.estimateSize()
    };
  }

  // Estimate memory usage
  estimateSize() {
    let size = 0;
    for (const [key, value] of this.shortTermMemory) {
      size += JSON.stringify([key, value]).length;
    }
    for (const [key, value] of this.longTermMemory) {
      size += JSON.stringify([key, value]).length;
    }
    for (const item of this.episodicMemory) {
      size += JSON.stringify(item).length;
    }
    // Add other memory types...
    return size;
  }

  // Clear memory of specific type
  clear(type = 'all') {
    switch (type) {
      case 'short':
        this.shortTermMemory.clear();
        break;
      case 'long':
        this.longTermMemory.clear();
        break;
      case 'episodic':
        this.episodicMemory = [];
        break;
      case 'semantic':
        this.semanticMemory.clear();
        break;
      case 'procedural':
        this.proceduralMemory.clear();
        break;
      case 'all':
      default:
        this.shortTermMemory.clear();
        this.longTermMemory.clear();
        this.episodicMemory = [];
        this.semanticMemory.clear();
        this.proceduralMemory.clear();
        break;
    }
    
    return { success: true, cleared: type };
  }
}

module.exports = MemorySystem;