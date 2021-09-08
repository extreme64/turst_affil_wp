<?php
global $ta_links_xml;



add_action( 'wp_dashboard_setup', 'posts_uris_to_xml' );
function posts_uris_to_xml() {
	$do_generate = false;
	if($do_generate){
		// global $post;
		$array = array();

		$posts = get_posts();
		// echo var_dump($posts[0]);
		foreach ($posts as $key => $post) {
			
			$array['link-'.$post->ID] = array(
				'attrs' => array(
					'post-id' => $post->ID, 
					'mod' => $post->post_modified,
					'mod_gmt' => $post->post_modified_gmt),
				'permalink' => get_post_permalink($post->ID),
				'post_title' => $post->post_title,
				'domain' => $_SERVER['HTTP_HOST']
			);
		}


		$file = get_template_directory() . "/ta_added_links.xml";


		$xml = new SimpleXMLElement("<?xml version=\"1.0\" encoding=\"utf-8\"?><root></root>");
		to_xml($xml, $array);

		
		$ta_links_xml = '<a href="' . get_template_directory_uri() . '/ta_added_links.xml">XML</a>';
	
	
		if ($xml->asXML($file)) {
			echo 'Saved! >> ';
		} else {
			echo 'Unable to save to file :(';
		}
		// print $xml->asXML();
		die;
	}
}

function to_xml(SimpleXMLElement $object, array $data)
{   
    foreach ($data as $key => $value) {
        if (is_array($value)) {
			if('attrs' === $key){
				continue;
			}
            $new_object = $object->addChild($key);
			$new_object->addAttribute('post-id', $value['attrs']['post-id']);
			$new_object->addAttribute('mod', $value['attrs']['mod']);
			$new_object->addAttribute('mod_gmt', $value['attrs']['mod_gmt']);
            to_xml($new_object, $value);
        } else {
            // if the key is an integer, it needs text with it to actually work.
            if ($key != 0 && $key == (int) $key) {
                $key = "key_$key";
            }

            $object->addChild($key, $value);
        }   
    }   
}


?>