//  JTSwiftPOC.swift
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

import UIKit

// This is a POC of how you can use JTLocalize in Swift
// These 2 methods should have been in the Pod itself, but until Swift support in CocoaPods goes out of beta, 
// this is the syntax.

func JTLocalizedString(key: String, comment: String) -> String { // genstrings will warn about this line, but it's fine
    return JTLocalize.localizedStringForKey(key, comment: comment)
}

func JTDynamicLocalizedString(key: String) -> String {
    return JTLocalize.localizedStringForKey(key, comment: "")
}

public class JTSwiftPOC: NSObject {
    public func foo() {
        let localizedString1 = JTLocalizedString("Swift test 1", "A simple swift test")
        let localizedString2 = NSString.localizedStringWithFormat(
            JTLocalizedString("Format: %@", "A swift test with format"), localizedString1)
        
        println(localizedString2)
    }
}
