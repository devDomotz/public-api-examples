package com.domotz.api.example_client.commands;

import com.jakewharton.fliptables.FlipTable;
import org.openapitools.client.ApiException;
import org.openapitools.client.api.DeviceApi;
import picocli.CommandLine;

import java.util.List;
import java.util.Map;


@CommandLine.Command(name = "devices", description = "Lists all the devices of the agent.")
public class DevicesList extends Command {
    @CommandLine.Option(names = {"-a", "--agent-id"}, description = "Agent ID ", required = true)
    private Integer agentId;

    @Override
    public Void call() throws ApiException {
        super.call();
        DeviceApi deviceApi = new DeviceApi(apiClient);
        List<Object> devices = deviceApi.listDevices(agentId, true);

        renderDevices(devices);

        return null;
    }


    private void renderDevices(List<Object> devices) {
        String[] headers = {"Id", "Display Name", "Protocol", "Status", "Importance"};
        String[][] data = new String[devices.size()][5];
        for (int i = 0; i < devices.size(); i++) {
            Map<String, Object> device = (Map<String, Object>) devices.get(i);
            data[i][0] = Integer.toString(((Double) device.get("id")).intValue());
            data[i][1] = device.get("display_name").toString();
            data[i][2] = device.get("protocol").toString();
            data[i][3] = device.get("status").toString();
            data[i][4] = device.get("importance").toString();
        }
        System.out.println(FlipTable.of(headers, data));
    }

}
