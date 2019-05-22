package com.domotz.api.example_client.commands;

import org.openapitools.client.ApiException;
import org.openapitools.client.api.AgentApi;
import org.openapitools.client.model.AgentDetail;
import picocli.CommandLine;

@CommandLine.Command(name = "agent", aliases = {"a"}, description = "Show the agent details.")
public class Agent extends Command {
    @CommandLine.Option(names = {"-a", "--agent-id"}, description = "Agent ID ", required = true)
    private Integer agentId;

    @Override
    public Void call() throws ApiException {
        super.call();
        AgentApi agentApi = new AgentApi(apiClient);
        AgentDetail agent = agentApi.getAgent(agentId);
        System.out.println(agent);
        return null;
    }

}
