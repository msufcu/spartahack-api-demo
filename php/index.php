<!doctype HTML>
<html>
    <head>
        <title>
            API Discovery Tool
        </title>
        <link rel="stylesheet" type="text/css" href="api.css" />
    </head>
    <body>
        <?php
        /*
         * To change this license header, choose License Headers in Project Properties.
         * To change this template file, choose Tools | Templates
         * and open the template in the editor.
         */

        function show_metadata($item) {
            echo "<h2>";
            foreach ($item['icons'] as $size => $icon) {
                echo "<img src='$icon' title='$size' />";
            }
            echo "$item[name] - $item[version]</h2>";
            echo "<p>$item[description]</p>";
            if (!empty($item['discoveryRestUrl'])) {
                echo "<a href='?url=$item[discoveryRestUrl]'>Discovery</a>";
                echo "<a href='$item[discoveryRestUrl]' target='_blank'>Discovery(raw)</a>";
            }
            if (!empty($item['documentationLink'])) {
                echo "<a href='$item[documentationLink]' target='_blank'>Developer Documentation</a>";
            }
        }

        $api_url = 'https://www.googleapis.com/discovery/v1/apis/';
        if (!empty($_GET['url'])) {
            $api_url = $_GET['url'];
        }
        $ch = curl_init($api_url);
        curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        $json = curl_exec($ch);
        if (curl_errno($ch) > 0) {
            echo curl_error($ch), "\n\n";
        } else {
            $data = json_decode($json, true);
            if (null == $data) {
                echo $json;
            } else {
                switch ($data['kind']) {
                    case 'discovery#directoryList' :

                        foreach ($data['items'] as $item) {
                            echo "<div>";
                            show_metadata($item);
                            echo '</div>';
                        }
                        break;
                    case 'discovery#restDescription' :
                        show_metadata($data);
                        echo "<table cellspacing='0' cellpadding='0'>";
                        foreach ($data as $key => $value) {
                            if (!is_array($value) && '' != $value) {
                                echo "<tr><td>$key</td><td>$value</td></tr>\n";
                            }
                        }
                        echo "</table>";

                        if (!empty($data['schemas'])) {
                            foreach ($data['schemas'] as $name => $schema) {
                                echo "<div><h3>$name</h3>";
                                if (!empty($schema['description'])) {
                                    echo "<p>$schema[description]</p>";
                                }
                                echo "</div>";
                            }
                        }
                        break;
                    default:

                        var_dump($data);
                        break;
                }
            }
        }
        ?>
    </body>
</html>