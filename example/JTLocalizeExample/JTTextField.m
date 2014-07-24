//
//  JTTextField.m
//  JTLocalizeExample
//
//  Created by Matan Eilat on 7/24/14.
//  Copyright (c) 2014 JoyTunes. All rights reserved.
//

#import "JTTextField.h"
#import "JTLocalizeUtils.h"

@implementation JTTextField

- (void)awakeFromNib {
    NSString *localizedPlaceholder = JTDynamicLocalizedString(self.placeholder);
    self.placeholder = localizedPlaceholder;
    NSString *localizedString = JTDynamicLocalizedString(self.text);
    self.text = localizedString;
}

@end
