package com.domotz.api.example_client.commands;

import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.api.AgentApi;
import picocli.CommandLine;

@CommandLine.Command(name = "agent_count", aliases = {"c"}, description = "Show the number of agents.")
public class AgentsCount extends Command {

    @Override
    public Void call() throws ApiException {
        super.call();
        ApiResponse<Void> response = new AgentApi(apiClient).countAgentsWithHttpInfo(null, null);
        String count = extractEntitiesCount(response);
        System.out.println(count);

        return null;
    }

}
