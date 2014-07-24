//
//  JTViewController.h
//  JTLocalizeExample
//
//  Created by Matan Eilat on 7/23/14.
//  Copyright (c) 2014 JoyTunes. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "JTLabel.h"
#import "JTButton.h"
#import "DTAttributedLabel+JTLocalizeExtensions.h"
#import "JTAttributedLabelWithLink.h"


@interface JTViewController : UIViewController

@property (strong, nonatomic) IBOutlet JTLabel *aLabel;
@property (strong, nonatomic) IBOutlet JTButton *aButton;
@property (strong, nonatomic) IBOutlet DTAttributedLabel *anAttributedLabel;
@property (strong, nonatomic) IBOutlet JTAttributedLabelWithLink *anAttributedLabelWithLink;


@end
