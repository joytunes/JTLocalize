//
//  JTButton.m
//  JTLocalizeExample
//
//  Created by Matan Eilat on 7/24/14.
//  Copyright (c) 2014 JoyTunes. All rights reserved.
//

#import "JTButton.h"
#import "JTLocalizeUtils.h"

@implementation JTButton


- (id)initWithFrame:(CGRect)frame {
    return [super initWithFrame:frame];
}

- (void)awakeFromNib {
    [super awakeFromNib];
    
    //This causes the button to resize text well, according to
    //http://stackoverflow.com/questions/6178545/adjust-uibutton-font-size-to-width
    self.titleLabel.numberOfLines = 1;
    self.titleLabel.adjustsFontSizeToFitWidth = YES;
    self.titleLabel.lineBreakMode = NSLineBreakByClipping;
    
    // Normal state
    [self setupTextForState:UIControlStateNormal];
    
    // Other control states
    if (self.customizeStates) {
        
        UIControlState controlStates[] = { UIControlStateDisabled, UIControlStateHighlighted, UIControlStateSelected };
        for (int i = 0; i < 3; i++) {
            [self setupTextForState:controlStates[i]];
        }
    }
    
    if (self.numberOfLines > 1) {
        self.titleLabel.numberOfLines = self.numberOfLines;
        self.titleLabel.lineBreakMode = NSLineBreakByWordWrapping;
    }
}

- (void)setupTextForState:(UIControlState)state {
    if ([self titleForState:state].length > 0) {
        NSString *localizedTitle = JTDynamicLocalizedString([self titleForState:state]);
        [self setTitle:localizedTitle forState:state];
    }
}




@end
