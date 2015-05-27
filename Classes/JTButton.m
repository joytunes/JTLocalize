// JTButton.m
//
// Copyright (c) 2015 JoyTunes (http://joytunes.com)
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

    UIControlState controlStates[] = { UIControlStateNormal, UIControlStateDisabled,
                                       UIControlStateHighlighted, UIControlStateSelected};
    for (int i = 0; i < 4; i++) {
        [self setupTextForState:controlStates[i]];
    }
}

- (void)setupTextForState:(UIControlState)state {
    NSString *title = [self titleForState:state];
    if ([self shouldLocalizeTitle:title forState:state]) {
        [self setTitle:title.localizedString forState:state];
    }

    NSAttributedString *attributedTitle = [self attributedTitleForState:state];
    if (attributedTitle.length > 0) {
        [self setAttributedTitle:attributedTitle.localizedAttributedStringByFragments forState:state];
    }
}

- (BOOL)shouldLocalizeTitle:(NSString *)title forState:(UIControlState)state {
    return title.length > 0 &&
            (state == UIControlStateNormal || ![title isEqualToString:[self titleForState:UIControlStateNormal]]);
}

@end
