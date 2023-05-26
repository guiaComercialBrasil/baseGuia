=== RSS Featured Image ===
Contributors: TigrouMeow
Tags: rss, featured, mailchimp, image, thumbnail, feed
Donate link: https://commerce.coinbase.com/checkout/d047546a-77a8-41c8-9ea9-4a950f61832f
Requires at least: 5.0
Tested up to: 5.3
Requires PHP: 5.0
Stable tag: 1.0.5

Add the featured image into your RSS feed (in the media:content). Works nicely with Mailchimp (*|RSSITEM:IMAGE|*). Light and simple, no options, no clutter in your WordPress.

== Description ==

RSS Featured Image adds the featured image into your RSS feed (in the media:content). It works nicely with Mailchimp (*|RSSITEM:IMAGE|*). In fact, it basically does the same thing as another (and more famous) plugin but without cluttering your WordPress Admin. This is a simple task, and I believe it should be invisible and run peacefuly in the background, with no impact on the UI and the overall WordPress performance.

=== Usage ===

By default, the size of the image is "large". I think it would be a shame to add new options to your WordPress admin only for this, so if you want to change the size, I propose you a filter :) You can include some code in your functions.php to take care of this. This is how you can use it:

function thumbnail_size_for_rss( $default ) {
  return 'thumbnail';
}
add_filter( 'rfi_rss_image_size', 'thumbnail_size_for_rss', 10, 1 );

== Installation ==

1. Upload `rss-featured-image` to the `/wp-content/plugins/` directory
2. Activate the plugin through the 'Plugins' menu in WordPress
3. That's all :) Can you believe it?

== Upgrade Notice ==

Replace all the files. Nothing else to do.

== Changelog ==

= 1.0.5 =
* Update: WordPress 5.0.
* Info: This plugin has currently no visibility on the WordPress Repository. If you like it, for its survival, please give it a nice review here: https://wordpress.org/support/plugin/rss-featured-image/reviews/?rate=5#new-post. Thanks a lot :)

= 1.0.4 =
* Update: WordPress 5.0.

= 1.0.0 =
* Add: Filter to choose the size.

= 0.0.1 =
* First release.
