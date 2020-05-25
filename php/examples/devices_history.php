<?php
require_once('vendor/autoload.php');
$agentId = $argv[1];
$baseUrl = $argv[2];
$apiKey = $argv[3];

$client = new \GuzzleHttp\Client();
$response = $client->request('GET', "$baseUrl/agent/$agentId/device", [
    'headers' => [
        'X-Api-Key' => $apiKey
    ]
]);

$devices = json_decode($response->getBody());

$history = [];
foreach ($devices as $device) {
    if ($device->protocol !== 'IP') {
        continue;
    }
    $deviceData = [$device->display_name, $device->vendor, $device->hw_address, $device->ip_addresses[0], $device->id];
    $response = $client->request('GET', "$baseUrl/agent/$agentId/device/$device->id/history/network/event", [
        'headers' => [
            'X-Api-Key' => $apiKey
        ]
    ]);

    $deviceHistory = json_decode($response->getBody());
    foreach ($deviceHistory as $event) {
        if($event->type !== 'UP' && $event->type != 'DOWN'){
            continue;
        }
        $row = array_merge([$event->timestamp, $event->type], $deviceData);
        $history = array_merge($history, [$row]);
    }
}
function cmp($a, $b) {
    return strcmp($a[0], $b[0]);
}
usort($history, 'cmp');
echo "Timestamp,Event,Name,Make,MAC Address,Main IP address,Id\n";
foreach($history as $item){
    echo "$item[0],$item[1],\"$item[2]\",\"$item[3]\",$item[4],$item[5],$item[6]\n";
}
