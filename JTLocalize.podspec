Pod::Spec.new do |s|
  s.name         = 'JTLocalize'
  s.version      = '0.1.1'
  s.license      = 'MIT'
  s.homepage     = 'https://github.com/joytunes/JTLocalize'
  s.authors      = { 'JoyTunes' => 'info@joytunes.com' }
  s.summary      = 'Localization infrastructure for iOS'
  s.source       = { :git => 'https://github.com/joytunes/JTLocalize.git', :tag => "0.1.0"}
  s.requires_arc = true

  s.ios.deployment_target = '6.0'

  s.source_files = 'Classes/*.{h,m}'

end
