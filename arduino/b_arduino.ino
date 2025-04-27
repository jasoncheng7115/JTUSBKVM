/*

=========================================================================

JTUSBKVM - Arduino Board B (Target Controller)

Version: 1.0.0
Last Update: 2024-11-18

Author: Jason Cheng
E-mail: jason@jason.tools
GitHub: https://github.com/jasoncheng7115

License: GNU Affero General Public License v3.0
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
any later version.

=========================================================================

*/

#include <HID-Project.h>

// 追蹤修飾鍵狀態
struct {
    bool ctrl: 1;
    bool shift: 1;
    bool alt: 1;
    bool meta: 1;  // Windows key
} modifierStates = {false, false, false, false};

void setup() {
    Serial1.begin(19200);
    NKROKeyboard.begin();
    AbsoluteMouse.begin();
}

void loop() {
    if (Serial1.available()) {
        String data = Serial1.readStringUntil('\n');
        data.trim();

        if (data.startsWith("KEY_DOWN ")) {
            String key = data.substring(9);
            processKeyEvent(key, true);
        } else if (data.startsWith("KEY_UP ")) {
            String key = data.substring(7);
            processKeyEvent(key, false);
        } else if (data.startsWith("MOD_DOWN ")) {
            String modifier = data.substring(9);
            processModifierEvent(modifier, true);
        } else if (data.startsWith("MOD_UP ")) {
            String modifier = data.substring(7);
            processModifierEvent(modifier, false);
        } else if (data.startsWith("MOUSE_MOVE_TO ")) {
            String coords = data.substring(14);
            int16_t absoluteX = 0, absoluteY = 0;
            sscanf(coords.c_str(), "%hd %hd", &absoluteX, &absoluteY);
            moveMouseTo(absoluteX, absoluteY);
        } else if (data.startsWith("MOUSE_DOWN ")) {
            String button = data.substring(11);
            pressMouseButton(button);
        } else if (data.startsWith("MOUSE_UP ")) {
            String button = data.substring(9);
            releaseMouseButton(button);
        } else if (data == "MOUSE_END") {
            AbsoluteMouse.end();
        } else if (data.startsWith("MOUSE_SCROLL ")) {
            String amount = data.substring(13);
            int8_t scrollAmount = amount.toInt();  // 確保使用整數
            AbsoluteMouse.move(0, 0, scrollAmount);  // 直接傳入整數值 
        } else if (data == "CTRL_ALT_DEL") {

            // 按下組合鍵
            NKROKeyboard.press(KEY_LEFT_CTRL);
            NKROKeyboard.press(KEY_LEFT_ALT);
            NKROKeyboard.press(KEY_DELETE);
            
            // 短暫延遲
            delay(100);
           
            // 釋放所有按鍵
            NKROKeyboard.releaseAll();

        } else if (data == "RELEASE_ALL") {
            // 新增：釋放所有按鍵和修飾鍵
            releaseAllModifiers();
            NKROKeyboard.releaseAll();
        }
    }
}

void releaseAllModifiers() {
    
    // 釋放所有修飾鍵
    if (modifierStates.ctrl) {
        NKROKeyboard.release(KEY_LEFT_CTRL);
        modifierStates.ctrl = false;
    }
    if (modifierStates.shift) {
        NKROKeyboard.release(KEY_LEFT_SHIFT);
        modifierStates.shift = false;
    }
    if (modifierStates.alt) {
        NKROKeyboard.release(KEY_LEFT_ALT);
        modifierStates.alt = false;
    }
    if (modifierStates.meta) {
        NKROKeyboard.release(KEY_LEFT_GUI);
        modifierStates.meta = false;
    }
}

void processKeyEvent(String key, bool isPress) {
    if (key.startsWith("Key") && key.length() == 4) {
        // 字母鍵
        char c = key.charAt(3);
        if (c >= 'A' && c <= 'Z') {
            if (isPress) {
                NKROKeyboard.write(c + 32); // 轉為小寫 ASCII
            }
        }
    } 
    else if (key.startsWith("Digit") && key.length() == 6) {
        // 數字鍵
        char c = key.charAt(5);
        if (c >= '0' && c <= '9') {
            if (isPress) {
                NKROKeyboard.write(c);
            }
        }
    }
    else if (key == "Control") {
        if (isPress) {
            NKROKeyboard.press(KEY_LEFT_CTRL);
        } else {
            NKROKeyboard.release(KEY_LEFT_CTRL);
        }
    }
    else if (key == "Alt") {
        if (isPress) {
            NKROKeyboard.press(KEY_LEFT_ALT);
        } else {
            NKROKeyboard.release(KEY_LEFT_ALT);
        }
    }
    else if (key == "Delete") {
        if (isPress) {
            NKROKeyboard.press(KEY_DELETE);
        } else {
            NKROKeyboard.release(KEY_DELETE);
        }
    }
    else if (key == "Meta") {  // Windows key
        if (isPress) {
            NKROKeyboard.press(KEY_LEFT_GUI);
        } else {
            NKROKeyboard.release(KEY_LEFT_GUI);
        }
    }
    else if (key.startsWith("F") && key.length() <= 3) {
        // F1-F12 功能鍵
        int fn = key.substring(1).toInt();
        if (fn >= 1 && fn <= 12) {
            if (isPress) {
                switch(fn) {
                    case 1: NKROKeyboard.press(KEY_F1); break;
                    case 2: NKROKeyboard.press(KEY_F2); break;
                    case 3: NKROKeyboard.press(KEY_F3); break;
                    case 4: NKROKeyboard.press(KEY_F4); break;
                    case 5: NKROKeyboard.press(KEY_F5); break;
                    case 6: NKROKeyboard.press(KEY_F6); break;
                    case 7: NKROKeyboard.press(KEY_F7); break;
                    case 8: NKROKeyboard.press(KEY_F8); break;
                    case 9: NKROKeyboard.press(KEY_F9); break;
                    case 10: NKROKeyboard.press(KEY_F10); break;
                    case 11: NKROKeyboard.press(KEY_F11); break;
                    case 12: NKROKeyboard.press(KEY_F12); break;
                }
            } else {
                switch(fn) {
                    case 1: NKROKeyboard.release(KEY_F1); break;
                    case 2: NKROKeyboard.release(KEY_F2); break;
                    case 3: NKROKeyboard.release(KEY_F3); break;
                    case 4: NKROKeyboard.release(KEY_F4); break;
                    case 5: NKROKeyboard.release(KEY_F5); break;
                    case 6: NKROKeyboard.release(KEY_F6); break;
                    case 7: NKROKeyboard.release(KEY_F7); break;
                    case 8: NKROKeyboard.release(KEY_F8); break;
                    case 9: NKROKeyboard.release(KEY_F9); break;
                    case 10: NKROKeyboard.release(KEY_F10); break;
                    case 11: NKROKeyboard.release(KEY_F11); break;
                    case 12: NKROKeyboard.release(KEY_F12); break;
                }
            }
        }
    }
    else {
        // 特殊鍵
        if (key == "Enter" && isPress) {
            NKROKeyboard.write(KEY_RETURN);
        }
        else if (key == "Backspace" && isPress) {
            NKROKeyboard.write(KEY_BACKSPACE);
        }
        else if (key == "Tab" && isPress) {
            NKROKeyboard.write(KEY_TAB);
        }
        else if (key == "Space" && isPress) {
            NKROKeyboard.write(' ');
        }
        else if (key == "Minus" && isPress) {
            NKROKeyboard.write('-');
        }
        else if (key == "Equal" && isPress) {
            NKROKeyboard.write('=');
        }
        else if (key == "BracketLeft" && isPress) {
            NKROKeyboard.write('[');
        }
        else if (key == "BracketRight" && isPress) {
            NKROKeyboard.write(']');
        }
        else if (key == "Backslash" && isPress) {
            NKROKeyboard.write('\\');
        }
        else if (key == "Semicolon" && isPress) {
            NKROKeyboard.write(';');
        }
        else if (key == "Quote" && isPress) {
            NKROKeyboard.write('\'');
        }
        else if (key == "Backquote" && isPress) {
            NKROKeyboard.write('`');
        }
        else if (key == "Comma" && isPress) {
            NKROKeyboard.write(',');
        }
        else if (key == "Period" && isPress) {
            NKROKeyboard.write('.');
        }
        else if (key == "Slash" && isPress) {
            NKROKeyboard.write('/');
        }
        else if (key == "Escape") {
            if (isPress) {
                NKROKeyboard.press(KEY_ESC);
            } else {
                NKROKeyboard.release(KEY_ESC);
            }
        }

        // 方向鍵與其它特殊鍵 press/release
        else if (key == "ArrowLeft") {
            if (isPress) NKROKeyboard.press(KEY_LEFT_ARROW);
            else NKROKeyboard.release(KEY_LEFT_ARROW);
        }
        else if (key == "ArrowRight") {
            if (isPress) NKROKeyboard.press(KEY_RIGHT_ARROW);
            else NKROKeyboard.release(KEY_RIGHT_ARROW);
        }
        else if (key == "ArrowUp") {
            if (isPress) NKROKeyboard.press(KEY_UP_ARROW);
            else NKROKeyboard.release(KEY_UP_ARROW);
        }
        else if (key == "ArrowDown") {
            if (isPress) NKROKeyboard.press(KEY_DOWN_ARROW);
            else NKROKeyboard.release(KEY_DOWN_ARROW);
        }

        // 編輯鍵區
        else if (key == "Insert") {
            if (isPress) NKROKeyboard.press(KEY_INSERT);
            else NKROKeyboard.release(KEY_INSERT);
        }
        else if (key == "Delete") {
            if (isPress) NKROKeyboard.press(KEY_DELETE);
            else NKROKeyboard.release(KEY_DELETE);
        }
        else if (key == "Home") {
            if (isPress) NKROKeyboard.press(KEY_HOME);
            else NKROKeyboard.release(KEY_HOME);
        }
        else if (key == "End") {
            if (isPress) NKROKeyboard.press(KEY_END);
            else NKROKeyboard.release(KEY_END);
        }
        else if (key == "PageUp") {
            if (isPress) NKROKeyboard.press(KEY_PAGE_UP);
            else NKROKeyboard.release(KEY_PAGE_UP);
        }
        else if (key == "PageDown") {
            if (isPress) NKROKeyboard.press(KEY_PAGE_DOWN);
            else NKROKeyboard.release(KEY_PAGE_DOWN);
        }
    }
}

void processModifierEvent(String modifier, bool isPress) {
    if (modifier == "Control") {
        if (isPress) {
            NKROKeyboard.press(KEY_LEFT_CTRL);
            modifierStates.ctrl = true;
        } else {
            NKROKeyboard.release(KEY_LEFT_CTRL);
            modifierStates.ctrl = false;
        }
    }
    else if (modifier == "Shift") {
        if (isPress) {
            NKROKeyboard.press(KEY_LEFT_SHIFT);
            modifierStates.shift = true;
        } else {
            NKROKeyboard.release(KEY_LEFT_SHIFT);
            modifierStates.shift = false;
        }
    }
    else if (modifier == "Alt") {
        if (isPress) {
            NKROKeyboard.press(KEY_LEFT_ALT);
            modifierStates.alt = true;
        } else {
            NKROKeyboard.release(KEY_LEFT_ALT);
            modifierStates.alt = false;
        }
    }
    else if (modifier == "Meta") {
        if (isPress) {
            NKROKeyboard.press(KEY_LEFT_GUI);
            modifierStates.meta = true;
        } else {
            NKROKeyboard.release(KEY_LEFT_GUI);
            modifierStates.meta = false;
        }
    }
}

void moveMouseTo(int16_t x, int16_t y) {
    if (x < -32768) x = -32768;
    if (x > 32767) x = 32767;
    if (y < -32768) y = -32768;
    if (y > 32767) y = 32767;
    
    AbsoluteMouse.moveTo(x, y);
}

void pressMouseButton(String button) {
    uint8_t btn = mapMouseButton(button);
    if (btn != 0) {
        AbsoluteMouse.press(btn);
    }
}

void releaseMouseButton(String button) {
    uint8_t btn = mapMouseButton(button);
    if (btn != 0) {
        AbsoluteMouse.release(btn);
    }
}

uint8_t mapMouseButton(String button) {
    if (button == "LEFT") return MOUSE_LEFT;
    if (button == "RIGHT") return MOUSE_RIGHT;
    if (button == "MIDDLE") return MOUSE_MIDDLE;
    return 0;
}
