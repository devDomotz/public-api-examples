package com.domotz.api.example_client.commands;

import com.jakewharton.fliptables.FlipTable;
import org.openapitools.client.ApiException;
import org.openapitools.client.api.UserApi;
import org.openapitools.client.model.User;
import picocli.CommandLine;

@CommandLine.Command(name = "user", description = "Show the user details.")
public class UserInfo extends Command {

    @Override
    public Void call() throws ApiException {
        super.call();
        User user = new UserApi(apiClient).getUser();

        String[] headers = {"Key", "Value"};
        System.out.println("User");
        System.out.println(FlipTable.of(headers, new String[][]{
                {"Name", user.getName()},
                {"ID", user.getId().toString()}
        }));

        return null;
    }
}
