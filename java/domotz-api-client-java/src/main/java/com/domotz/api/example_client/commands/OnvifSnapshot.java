package com.domotz.api.example_client.commands;

import org.openapitools.client.ApiException;
import org.openapitools.client.api.MultimediaApi;
import picocli.CommandLine;

import java.io.FileInputStream;
import java.io.IOException;

@CommandLine.Command(name = "snapshot", description = "Gets a snapshot from an onvif camera.")
public class OnvifSnapshot extends Command {
    @CommandLine.Option(names = {"-a", "--agent-id"}, description = "Agent ID ", required = true)
    private Integer agentId;
    @CommandLine.Option(names = {"-d", "--device-id"}, description = "Device ID ", required = true)
    private Integer id;

    @Override
    public Void call() throws ApiException {
        super.call();

        MultimediaApi multimediaApi = new MultimediaApi(apiClient);
        try {
            FileInputStream fis = new FileInputStream(multimediaApi.onvifSnapshot(agentId, id));
            byte[] buf = new byte[1024];
            int hasRead = 0;
            while ((hasRead = fis.read(buf)) > 0) {
                System.out.write(buf, 0, hasRead);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        return null;
    }
}