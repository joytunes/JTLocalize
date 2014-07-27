// JTButton.m
//
// Copyright (c) 2014 JoyTunes (http://joytunes.com)
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
// THE SOFTWARE.

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
