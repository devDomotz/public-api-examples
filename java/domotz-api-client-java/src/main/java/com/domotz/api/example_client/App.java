package com.domotz.api.example_client;

import com.domotz.api.example_client.commands.*;
import org.openapitools.client.ApiClient;
import picocli.CommandLine;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

@CommandLine.Command(subcommands = {
        Agent.class,
        AgentsCount.class,
        AgentsList.class,
        DevicesList.class,
        Device.class,
        UserInfo.class,
        SetDeviceField.class,
        OnvifSnapshot.class
}, name = "domotz-example-api-client"
)
public class App {
    enum SHARDS {
        US, EU, dev
    }

    public static final Map<SHARDS, String> servers;

    static {
        Map<SHARDS, String> tmp = new HashMap<>();
        tmp.put(SHARDS.US, "https://api-us-east-1-cell-1.domotz.com/public-api/v1");
        tmp.put(SHARDS.EU, "https://api-eu-west-1-cell-1.domotz.com/public-api/v1");
        tmp.put(SHARDS.dev, "http://127.0.0.1:8888/public-api/v1");
        servers = Collections.unmodifiableMap(tmp);
    }

    @CommandLine.Option(names = {"-v", "--verbose"}, description = "Be verbose.")
    private boolean verbose = false;
    @CommandLine.Option(names = {"-k", "--api-key"}, description = "API key", required = true)
    public String apiKey;
    @CommandLine.Option(names = {"-c", "--cell"}, description = "The shard, either US or EU", required = true)
    public SHARDS cell;
    @CommandLine.Option(names = "--help", usageHelp = true, description = "Display this help and exit")
    private boolean help;

    public static void main(String[] args) {
        App main = new App();
        final ApiClient apiClient = org.openapitools.client.Configuration.getDefaultApiClient();

        CommandLine commandLine = new CommandLine(main, new CommandLine.IFactory() {
            @Override
            public <K> K create(Class<K> aClass) throws Exception {
                K ret = aClass.newInstance();
                ((Command) ret).setApiClient(apiClient);
                return ret;
            }
        });
        commandLine.parseWithHandler(new CommandLine.RunLast(), args);

    }
}