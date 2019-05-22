package com.domotz.api.example_client.commands;

import com.jakewharton.fliptables.FlipTable;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import org.openapitools.client.api.AgentApi;
import org.openapitools.client.model.AgentBase;
import picocli.CommandLine;

import java.util.ArrayList;
import java.util.List;

@CommandLine.Command(name = "agents", description = "Lists all the agents.")
public class AgentsList extends Command {

    private static final int SIZE = 100;


    @Override
    public Void call() throws ApiException {
        super.call();
        AgentApi agentApi = new AgentApi(apiClient);
        int count = getAgentsCount(agentApi);
        List<AgentBase> agents = fetchAgentsPaginated(agentApi, count);
        renderAgents(agents);

        return null;
    }

    private void renderAgents(List<AgentBase> agents) {
        String[] headers = {"Id", "Display Name", "Api Enabled", "Creation Time", "Bound Mac Address", "Status"};
        String[][] data = new String[agents.size()][6];
        for (int i = 0; i < agents.size(); i++) {
            AgentBase agent = agents.get(i);
            data[i][0] = agent.getId().toString();
            data[i][1] = agent.getDisplayName();
            data[i][2] = agent.getAccessRight().getApiEnabled() ? "YES" : "NO";
            data[i][3] = agent.getCreationTime().toString();
            data[i][4] = agent.getLicence().getBoundMacAddress();
            data[i][5] = agent.getStatus().getValue().toString();
        }
        System.out.println(FlipTable.of(headers, data));
    }

    private List<AgentBase> fetchAgentsPaginated(AgentApi agentApi, int count) throws ApiException {
        int pages = calculatePagesNumber(count);
        System.out.printf("Fetching %s agents in %s pages%n", count, pages);

        int pageNumber = 0;
        List<AgentBase> agents = new ArrayList<>(count);
        while (pageNumber < pages) {
            List<AgentBase> temp = agentApi.listAgents(SIZE, pageNumber, null, null);
            agents.addAll(temp);
            pageNumber++;
            System.out.printf("Fetched %s agents - page %s%n", temp.size(), pageNumber);
        }
        return agents;
    }

    private int calculatePagesNumber(int count) {
        return count / SIZE + ((count % SIZE != 0) ? 1 : 0);
    }

    private int getAgentsCount(AgentApi agentApi) throws ApiException {
        ApiResponse<Void> response = agentApi.countAgentsWithHttpInfo(null, null);
        return Integer.parseInt(extractEntitiesCount(response));
    }
}
