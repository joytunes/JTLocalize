//
//  JTSwiftPOC.swift
//  JTLocalizeExample
//
//  Created by Yoni Tsafir on 3/3/15.
//  Copyright (c) 2015 JoyTunes. All rights reserved.
//

import UIKit

// This is a POC of how you can use JTLocalize in Swift
// These 2 methods should have been in the Pod itself, but until Swift support in CocoaPods goes out of beta, 
// this is the syntax.

func JTLocalizedString(key: String, comment: String) -> String {
    return JTLocalize.localizedStringForKey(key, comment: comment)
}

func JTDynamicLocalizedString(key: String) -> String {
    return JTLocalizedString(key, "")
}

public class JTSwiftPOC: NSObject {
    public func foo() {
        let localizedString1 = JTLocalizedString("Swift test 1", "A simple swift test")
        let localizedString2 = NSString.localizedStringWithFormat(
            JTLocalizedString("Format: %@", "A swift test with format"), localizedString1)
        
        println(localizedString2)
    }
}
