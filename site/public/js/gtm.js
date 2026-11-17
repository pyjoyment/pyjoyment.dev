// The snippet of Google Tag Manager, which the layout loads before gtm.js, in
// a file of its own, as Content-Security-Policy takes no inline script
window.dataLayer = window.dataLayer || [];
function gtag() {
  // biome-ignore lint/complexity/noArguments: the tag of Google takes a command as the object Arguments, not an array
  window.dataLayer.push(arguments);
}
gtag("js", new Date());
