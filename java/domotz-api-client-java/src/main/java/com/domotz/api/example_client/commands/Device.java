package com.domotz.api.example_client.commands;

import org.openapitools.client.ApiException;
import org.openapitools.client.api.DeviceApi;
import picocli.CommandLine;

@CommandLine.Command(name = "device", description = "Show the device details.")
public class Device extends Command {
    @CommandLine.Option(names = {"-a", "--agent-id"}, description = "Agent ID ", required = true)
    private Integer agentId;
    @CommandLine.Option(names = {"-d", "--device-id"}, description = "Device ID ", required = true)
    private Integer id;

    @Override
    public Void call() throws ApiException {
        super.call();

        DeviceApi deviceApi = new DeviceApi(apiClient);
        System.out.println(deviceApi.getDevice(agentId, id));

        return null;
    }
}