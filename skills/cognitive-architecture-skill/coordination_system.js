// Cognitive Architecture - Coordination System Component
// Multi-agent coordination and task management

class CoordinationSystem {
  constructor(options = {}) {
    this.agents = new Map(); // agentId -> agent instance
    this.pendingTasks = [];
    this.activeTasks = new Map(); // taskId -> { task, assignedAgentId, startTime, deadline }
    this.messages = []; // Message queue
    this.resourcePool = {}; // Shared resources
    this.agreementRegistry = new Map(); // Contract/Agreement registry
    this.options = {
      maxMessageHistory: options.maxMessageHistory || 1000,
      taskTimeout: options.taskTimeout || 300000, // 5 minutes default
      ...options
    };
  }

  // Register a new agent
  async registerAgent(agent) {
    // Validate agent interface
    if (!agent.id || !agent.name || !agent.capabilities) {
      throw new Error('Agent must have id, name, and capabilities');
    }
    
    this.agents.set(agent.id, agent);
    console.log(`Agent ${agent.name} (${agent.id}) registered`);
    
    // Notify other agents of new member
    await this.broadcastMessage({
      type: 'agent_joined',
      agentId: agent.id,
      agentName: agent.name,
      capabilities: agent.capabilities,
      timestamp: new Date().toISOString()
    });
    
    return { 
      success: true, 
      agentId: agent.id,
      message: `Agent ${agent.name} successfully registered`
    };
  }

  // Unregister an agent
  async unregisterAgent(agentId) {
    const agent = this.agents.get(agentId);
    if (!agent) {
      return { success: false, error: 'Agent not found' };
    }
    
    // Reassign tasks if any were assigned to this agent
    for (const [taskId, taskInfo] of this.activeTasks.entries()) {
      if (taskInfo.assignedAgentId === agentId) {
        this.reassignTask(taskId);
      }
    }
    
    // Remove agent
    this.agents.delete(agentId);
    console.log(`Agent ${agentId} unregistered`);
    
    // Notify other agents
    await this.broadcastMessage({
      type: 'agent_left',
      agentId: agentId,
      timestamp: new Date().toISOString()
    });
    
    return { success: true, message: `Agent ${agentId} unregistered` };
  }

  // Assign a task to an appropriate agent
  async assignTask(task) {
    // Find suitable agent based on capabilities and availability
    const suitableAgents = Array.from(this.agents.values())
      .filter(agent => 
        this.agentCanHandleTask(agent, task) && 
        agent.status === 'idle'
      );
    
    if (suitableAgents.length > 0) {
      // Select agent (simple round-robin for now, could be more sophisticated)
      const selectedAgent = suitableAgents[0];
      
      // Create task ID
      const taskId = `task_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      
      // Mark task as active
      this.activeTasks.set(taskId, {
        task,
        assignedAgentId: selectedAgent.id,
        startTime: new Date(),
        deadline: task.deadline || new Date(Date.now() + this.options.taskTimeout)
      });
      
      console.log(`Assigned task "${task.description}" to agent ${selectedAgent.name}`);
      
      // Execute the task asynchronously
      const executionPromise = this.executeTaskOnAgent(selectedAgent, task, taskId);
      
      // Handle task completion
      executionPromise.then(result => {
        this.completeTask(taskId, result);
      }).catch(error => {
        this.failTask(taskId, error);
      });
      
      return {
        taskId,
        assignedAgentId: selectedAgent.id,
        assignedAgentName: selectedAgent.name,
        status: 'assigned',
        message: `Task assigned to agent ${selectedAgent.name}`
      };
    } else {
      // No suitable agent available, add to pending
      const taskId = `task_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      this.pendingTasks.push({ 
        taskId, 
        task, 
        submittedAt: new Date(),
        retries: 0
      });
      
      console.log(`Task "${task.description}" added to pending queue`);
      
      // Schedule retry when agents become available
      this.schedulePendingTaskProcessing();
      
      return {
        taskId,
        status: 'pending',
        message: 'No suitable agent available, added to queue'
      };
    }
  }

  // Check if agent can handle a specific task
  agentCanHandleTask(agent, task) {
    if (!task.requiredCapabilities) return true;
    
    return task.requiredCapabilities.every(reqCap => 
      agent.capabilities.some(agentCap => agentCap === reqCap)
    );
  }

  // Execute task on a specific agent
  async executeTaskOnAgent(agent, task, taskId) {
    try {
      agent.status = 'working';
      const result = await agent.executeTask(task);
      agent.status = 'idle';
      
      return {
        taskId,
        agentId: agent.id,
        result,
        completedAt: new Date().toISOString(),
        success: true
      };
    } catch (error) {
      agent.status = 'idle';
      
      return {
        taskId,
        agentId: agent.id,
        error: error.message,
        completedAt: new Date().toISOString(),
        success: false
      };
    }
  }

  // Complete a task
  completeTask(taskId, result) {
    const taskInfo = this.activeTasks.get(taskId);
    if (taskInfo) {
      this.activeTasks.delete(taskId);
      
      // Log completion
      console.log(`Task ${taskId} completed by agent ${taskInfo.assignedAgentId}`);
      
      // Notify interested parties
      this.broadcastMessage({
        type: 'task_completed',
        taskId,
        result,
        completedBy: taskInfo.assignedAgentId,
        timestamp: new Date().toISOString()
      });
    }
  }

  // Fail a task
  failTask(taskId, error) {
    const taskInfo = this.activeTasks.get(taskId);
    if (taskInfo) {
      this.activeTasks.delete(taskId);
      
      console.log(`Task ${taskId} failed: ${error.message}`);
      
      // Notify interested parties
      this.broadcastMessage({
        type: 'task_failed',
        taskId,
        error: error.message,
        failedBy: taskInfo.assignedAgentId,
        timestamp: new Date().toISOString()
      });
    }
  }

  // Process pending tasks
  async processPendingTasks() {
    if (this.pendingTasks.length === 0) return;

    const remainingTasks = [];
    for (const pending of this.pendingTasks) {
      // Check if task has timed out
      if (pending.submittedAt && Date.now() - pending.submittedAt > this.options.taskTimeout * 3) {
        // Task has been pending too long, mark as failed
        this.broadcastMessage({
          type: 'task_timeout',
          taskId: pending.taskId,
          message: 'Task timed out in pending queue',
          timestamp: new Date().toISOString()
        });
        continue;
      }
      
      // Try to assign the task
      const suitableAgents = Array.from(this.agents.values())
        .filter(agent => 
          this.agentCanHandleTask(agent, pending.task) && 
          agent.status === 'idle'
        );
      
      if (suitableAgents.length > 0) {
        const selectedAgent = suitableAgents[0];
        
        // Create new task ID since the old one was for pending
        const taskId = `task_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        
        // Mark task as active
        this.activeTasks.set(taskId, {
          task: pending.task,
          assignedAgentId: selectedAgent.id,
          startTime: new Date(),
          deadline: pending.task.deadline || new Date(Date.now() + this.options.taskTimeout)
        });
        
        console.log(`Assigned pending task "${pending.task.description}" to agent ${selectedAgent.name}`);
        
        // Execute the task asynchronously
        const executionPromise = this.executeTaskOnAgent(selectedAgent, pending.task, taskId);
        
        executionPromise.then(result => {
          this.completeTask(taskId, result);
        }).catch(error => {
          this.failTask(taskId, error);
        });
      } else {
        // Still no suitable agent, keep in pending but increment retries
        pending.retries = (pending.retries || 0) + 1;
        
        // If retried too many times, consider escalation
        if (pending.retries < 5) { // Max 5 retries
          remainingTasks.push(pending);
        } else {
          // Escalate or fail
          this.broadcastMessage({
            type: 'task_esc_failed',
            taskId: pending.taskId,
            message: 'Task failed after multiple retries',
            timestamp: new Date().toISOString()
          });
        }
      }
    }
    
    this.pendingTasks = remainingTasks;
  }

  // Schedule processing of pending tasks
  schedulePendingTaskProcessing() {
    // Only schedule if not already scheduled
    if (!this.pendingTaskTimer) {
      this.pendingTaskTimer = setTimeout(async () => {
        await this.processPendingTasks();
        this.pendingTaskTimer = null;
        
        // If there are still pending tasks, reschedule
        if (this.pendingTasks.length > 0) {
          this.schedulePendingTaskProcessing();
        }
      }, 5000); // Try every 5 seconds
    }
  }

  // Reassign a task to a different agent
  reassignTask(taskId) {
    const taskInfo = this.activeTasks.get(taskId);
    if (!taskInfo) {
      return { success: false, error: 'Task not found' };
    }

    // Find alternative agent
    const suitableAgents = Array.from(this.agents.values())
      .filter(agent => 
        this.agentCanHandleTask(agent, taskInfo.task) && 
        agent.id !== taskInfo.assignedAgentId &&
        agent.status === 'idle'
      );
    
    if (suitableAgents.length > 0) {
      const oldAgentId = taskInfo.assignedAgentId;
      const newAgent = suitableAgents[0];
      
      taskInfo.assignedAgentId = newAgent.id;
      console.log(`Task ${taskId} reassigned from agent ${oldAgentId} to ${newAgent.name}`);
      
      // Notify about reassignment
      this.broadcastMessage({
        type: 'task_reassigned',
        taskId,
        fromAgent: oldAgentId,
        toAgent: newAgent.id,
        timestamp: new Date().toISOString()
      });
      
      return {
        success: true,
        taskId,
        newAgentId: newAgent.id,
        message: `Task reassigned to agent ${newAgent.id}`
      };
    } else {
      console.log(`Could not reassign task ${taskId}, no suitable agents available`);
      return {
        success: false,
        taskId,
        message: 'No suitable agents available for reassignment'
      };
    }
  }

  // Send message between agents
  sendMessage(fromAgentId, toAgentId, message) {
    const toAgent = this.agents.get(toAgentId);
    if (!toAgent) {
      return { success: false, error: 'Recipient agent not found' };
    }

    // Add metadata to message
    const fullMessage = {
      id: `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      from: fromAgentId,
      to: toAgentId,
      content: message,
      sentAt: new Date().toISOString(),
      protocolVersion: '1.0'
    };

    // Add to message history
    this.messages.push(fullMessage);
    if (this.messages.length > this.options.maxMessageHistory) {
      this.messages = this.messages.slice(-this.options.maxMessageHistory);
    }

    // Deliver message
    try {
      const result = toAgent.receiveMessage(fromAgentId, fullMessage);
      
      return {
        success: true,
        messageId: fullMessage.id,
        delivered: true,
        to: toAgentId,
        result
      };
    } catch (error) {
      return {
        success: false,
        messageId: fullMessage.id,
        error: error.message
      };
    }
  }

  // Broadcast message to all agents
  async broadcastMessage(message) {
    const fullMessage = {
      id: `broadcast_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      type: message.type,
      content: message,
      sentAt: new Date().toISOString(),
      from: 'COORDINATION_SYSTEM',
      protocolVersion: '1.0'
    };

    // Add to message history
    this.messages.push(fullMessage);
    if (this.messages.length > this.options.maxMessageHistory) {
      this.messages = this.messages.slice(-this.options.maxMessageHistory);
    }

    const results = [];
    for (const [agentId, agent] of this.agents) {
      try {
        const result = agent.receiveMessage(fullMessage.from, fullMessage);
        results.push({ agentId, result, success: true });
      } catch (error) {
        console.error(`Error broadcasting to agent ${agentId}: ${error.message}`);
        results.push({ 
          agentId, 
          error: error.message, 
          success: false 
        });
      }
    }
    
    return {
      messageId: fullMessage.id,
      recipients: this.agents.size,
      successful: results.filter(r => r.success).length,
      failed: results.filter(r => !r.success).length,
      results
    };
  }

  // Create an agreement/contract between agents
  createAgreement(participants, terms, duration, metadata = {}) {
    const agreementId = `agr_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    
    const agreement = {
      agreementId,
      participants,
      terms,
      duration,
      metadata,
      status: 'active',
      createdAt: new Date().toISOString(),
      signatures: {},
      version: 1
    };
    
    this.agreementRegistry.set(agreementId, agreement);
    
    // Notify participants
    for (const participantId of participants) {
      this.sendMessage('COORDINATION_SYSTEM', participantId, {
        type: 'agreement_created',
        agreementId,
        terms,
        timestamp: new Date().toISOString()
      });
    }
    
    return {
      success: true,
      agreementId,
      message: 'Agreement created and distributed to participants'
    };
  }

  // Get system status
  getStatus() {
    const agentStatuses = Array.from(this.agents.entries()).map(([id, agent]) => ({
      id: agent.id,
      name: agent.name,
      status: agent.status,
      capabilities: agent.capabilities,
      lastSeen: agent.lastSeen || 'unknown'
    }));

    return {
      totalAgents: this.agents.size,
      pendingTasks: this.pendingTasks.length,
      activeTasks: this.activeTasks.size,
      totalMessages: this.messages.length,
      activeAgreements: this.agreementRegistry.size,
      agents: agentStatuses,
      timestamp: new Date().toISOString()
    };
  }

  // Get task status
  getTaskStatus(taskId) {
    const activeTask = this.activeTasks.get(taskId);
    if (activeTask) {
      return {
        taskId,
        status: 'active',
        assignedAgentId: activeTask.assignedAgentId,
        startTime: activeTask.startTime,
        elapsed: Date.now() - activeTask.startTime.getTime(),
        deadline: activeTask.deadline
      };
    }
    
    // Check if it's a pending task
    const pendingTask = this.pendingTasks.find(t => t.taskId === taskId);
    if (pendingTask) {
      return {
        taskId,
        status: 'pending',
        submittedAt: pendingTask.submittedAt,
        retries: pendingTask.retries || 0
      };
    }
    
    return {
      taskId,
      status: 'not_found',
      message: 'Task not found in active or pending queues'
    };
  }

  // Cancel a pending task
  cancelPendingTask(taskId) {
    const initialLength = this.pendingTasks.length;
    this.pendingTasks = this.pendingTasks.filter(t => t.taskId !== taskId);
    
    if (this.pendingTasks.length < initialLength) {
      // Task was removed from pending
      return {
        success: true,
        taskId,
        message: 'Pending task cancelled'
      };
    } else {
      return {
        success: false,
        taskId,
        message: 'Task not found in pending queue'
      };
    }
  }
}

module.exports = CoordinationSystem;