package com.domotz.api.example_client.commands;

import com.domotz.api.example_client.App;
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.ApiResponse;
import picocli.CommandLine;

import java.util.List;
import java.util.Map;
import java.util.concurrent.Callable;


public abstract class Command implements Callable<Void> {
    @CommandLine.ParentCommand
    private App parent;
    protected ApiClient apiClient;

    public void setApiClient(ApiClient apiClient) {
        this.apiClient = apiClient;
    }

    public Void call() throws ApiException {
        this.apiClient.setApiKey(parent.apiKey);
        this.apiClient.setBasePath(App.servers.get(parent.cell));
        return null;
    }

    String extractEntitiesCount(ApiResponse<Void> response) {
        String count = null;
        for (Map.Entry<String, List<String>> entry : response.getHeaders().entrySet()) {
            if (entry.getKey().equalsIgnoreCase("x-entities-count")) {
                count = entry.getValue().get(0);
                break;
            }
        }
        return count;
    }
}
