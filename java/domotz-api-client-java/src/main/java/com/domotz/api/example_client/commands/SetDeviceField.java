package com.domotz.api.example_client.commands;

import org.openapitools.client.ApiException;
import org.openapitools.client.api.DeviceApi;
import picocli.CommandLine;

import java.util.Arrays;
import java.util.Collections;
import java.util.HashSet;
import java.util.Set;

@CommandLine.Command(name = "device_edit", description = "Edit the device details.")
public class SetDeviceField extends Command {
    final public Set<String> allowed = Collections.unmodifiableSet(new HashSet<>(Arrays.asList(
            "user_data/vendor",
            "details/zone",
            "importance",
            "details/room",
            "user_data/name",
            "user_data/type",
            "user_data/model"
    )));
    @CommandLine.Option(names = {"-a", "--agent-id"}, description = "Agent ID ", required = true)
    private Integer agentId;
    @CommandLine.Option(names = {"-d", "--device-id"}, description = "Device ID ", required = true)
    private Integer id;
    @CommandLine.Parameters(index = "0", description = "One of \"user_data/vendor\",\n" +
            "            \"details/zone\",\n" +
            "            \"importance\",\n" +
            "            \"details/room\",\n" +
            "            \"user_data/name\",\n" +
            "            \"user_data/type\",\n" +
            "            \"user_data/model\"")
    private String field;
    @CommandLine.Parameters(index = "1", description = "New value")
    private String value;


    @Override
    public Void call() throws ApiException {
        super.call();
        if (!allowed.contains(field)) {
            throw new RuntimeException("Cannot modify field " + field);
        }

        DeviceApi deviceApi = new DeviceApi(apiClient);
        deviceApi.editDevice(agentId, id, field, value);

        return null;
    }
}