//
//  JTAttributedLabelWithLink.m
//  JTLocalizeExample
//
//  Created by Matan Eilat on 7/24/14.
//  Copyright (c) 2014 JoyTunes. All rights reserved.
//


#import "JTAttributedLabelWithLink.h"


@interface JTAttributedLabelWithLink()<DTAttributedTextContentViewDelegate>

@end

@implementation JTAttributedLabelWithLink

- (id)initWithFrame:(CGRect)frame {
	self = [super initWithFrame:frame];
	
	if (self) {
		[self setupConnections];
	}
	
	return self;
}

- (void) awakeFromNib {
	[super awakeFromNib];
	[self setupConnections];
}

- (void)setupConnections {
    self.delegate = self;
    self.shouldDrawLinks = NO;
}

- (UIView *)attributedTextContentView:(DTAttributedTextContentView *)attributedTextContentView viewForLink:(NSURL *)url identifier:(NSString *)identifier frame:(CGRect)frame {
	DTLinkButton *button = [[DTLinkButton alloc] initWithFrame:frame];
	button.URL = url;
	button.minimumHitSize = CGSizeMake(25, 25); // adjusts it's bounds so that button is always large enough
	button.GUID = identifier;
	
	// get image with normal link text
	UIImage *normalImage = [attributedTextContentView contentImageWithBounds:frame options:DTCoreTextLayoutFrameDrawingDefault];
	[button setImage:normalImage forState:UIControlStateNormal];
	
	// get image for highlighted link text
	UIImage *highlightImage = [attributedTextContentView contentImageWithBounds:frame options:DTCoreTextLayoutFrameDrawingDrawLinksHighlighted];
	[button setImage:highlightImage forState:UIControlStateHighlighted];
	
	// use normal push action for opening URL
	[button addTarget:self action:@selector(linkPushed:) forControlEvents:UIControlEventTouchUpInside];
	
	return button;
}

- (void)linkPushed:(DTLinkButton *)button
{
	NSURL *URL = button.URL;
	[self.linkDelegate label:self clickedOnUrl:URL];
}

@end
