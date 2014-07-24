//
//  JTAttributedLabelWithLink.h
//  JTLocalizeExample
//
//  Created by Matan Eilat on 7/24/14.
//  Copyright (c) 2014 JoyTunes. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "DTCoreText.h"
#import "DTAttributedLabel+JTLocalizeExtensions.h"


@protocol DTLabelLinkDelegate <NSObject>

- (void)label:(id)sender clickedOnUrl:(NSURL *)url;

@end

@interface JTAttributedLabelWithLink : DTAttributedLabel

@property (nonatomic, weak) IBOutlet id<DTLabelLinkDelegate> linkDelegate;

@end
