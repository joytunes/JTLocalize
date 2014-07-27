Pod::Spec.new do |s|
  s.name         = 'JTLocalize'
  s.version      = '1.0.0'
  s.license      = 'MIT'
  s.homepage     = 'https://github.com/joytunes/JTLocalize.git'
  s.authors      = { 'JoyTunes' => 'info@joytunes.com' }
  s.summary      = 'Localization infrastructure for iOS'
  s.source       = { :git => 'https://github.com/joytunes/JTLocalize.git'}
  s.requires_arc = true

  s.ios.deployment_target = '6.0'

  s.public_header_files = 'JTLocalize/*.h'
  s.source_files = 'JTLocalize/JTLocalize.{h,m}'


end
