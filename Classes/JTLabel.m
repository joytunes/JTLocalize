// JTLabel.m
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

#import "JTLabel.h"
#import "JTLocalizeUtils.h"

@implementation JTLabel


- (id)initWithFrame:(CGRect)frame
{
    self = [super initWithFrame:frame];
    if (self) {
        // Initialization code
    }
    return self;
}

- (BOOL)isAttributedString {
    //IOS 6 fix : Treat all strings as attributed, or single-section attributed strings
    //will lose their formatting
    if ([[UIDevice currentDevice].systemVersion floatValue] < 7.0) {
        return !self.forceNonAttrStringInIOS6;
    }
    
    //Even if setting a normal text, attributed text will return a real matching object.
    //Must check for multiple attribute fragments to see if really attributed
    NSRange range;
    if (self.attributedText.length == 0) {
        return NO;
    }
    [self.attributedText attributesAtIndex:0 effectiveRange:&range];
    return range.length < self.attributedText.length;
}

- (void)awakeFromNib {
    if ([self isAttributedString]) {
        //Divide the string into fragments equivalent to the XIBs by asking for the effective range
        //of an attribute set (which map into a fragment in the xib).
        //For each such range, extract the string, localize and inject back inside.
        NSMutableAttributedString *attributedText = self.attributedText.mutableCopy;
        NSRange range;
        NSInteger startIndex = attributedText.length - 1;
        while (startIndex > 0) {
            [attributedText attributesAtIndex:startIndex effectiveRange:&range];
            NSString *fragment = [attributedText attributedSubstringFromRange:range].string;
            NSString *localizedFragment = JTDynamicLocalizedString(fragment);
            [attributedText replaceCharactersInRange:range withString:localizedFragment];
            startIndex = range.location - 1;
        }
        self.attributedText = attributedText;
    } else {
        NSString *localizedString = JTDynamicLocalizedString(self.text);
        self.text = localizedString;
    }
}

- (void)setStrokeColor:(UIColor *)strokeColor
{
    _strokeColor = strokeColor;
    [self setNeedsDisplay];
}

- (void)setStrokeWidth:(CGFloat)strokeWidth
{
    _strokeWidth = strokeWidth;
    [self setNeedsDisplay];
}

- (void)drawTextInRect:(CGRect)rect
{
    if (self.text == nil || self.strokeWidth == 0) {
        [super drawTextInRect:rect];
        return;
    }
    
    NSString *origText = self.text;
    
    //If aligning to the sides, add a space for the stroke
    if (self.textAlignment == NSTextAlignmentLeft) {
        self.text = [@" " stringByAppendingString:self.text];
    } else if (self.textAlignment == NSTextAlignmentRight) {
        self.text = [self.text stringByAppendingString:@" "];
    }
    
    
    CGSize shadowOffset = self.shadowOffset;
    UIColor *textColor = self.textColor;
    
    CGContextRef c = UIGraphicsGetCurrentContext();
    CGContextSetLineWidth(c, self.strokeWidth);
    CGContextSetLineJoin(c, kCGLineJoinRound);
    
    CGContextSetTextDrawingMode(c, kCGTextStroke);
    self.textColor = self.strokeColor;
    [super drawTextInRect:rect];
    
    CGContextSetTextDrawingMode(c, kCGTextFill);
    self.textColor = textColor;
    self.shadowOffset = CGSizeMake(0, 0);
    [super drawTextInRect:rect];
    
    self.shadowOffset = shadowOffset;
    self.text = origText;
}
@end
