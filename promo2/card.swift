// Genera las tarjetas de servicio del promo (1280x720, RGBA) usando CoreText:
//   card <salida.png> <indice> <total> <titulo>
// Usa CoreText para que el árabe (RTL + shaping) y el CJK se dibujen bien,
// cosa que PIL/raqm no hace en esta máquina.
import Foundation
import AppKit
import CoreText

let W: CGFloat = 1280, H: CGFloat = 720
let RED = NSColor(srgbRed: 1.0, green: 31.0/255.0, blue: 31.0/255.0, alpha: 1)

func fontFor(_ s: String, size: CGFloat) -> NSFont {
    let u = Array(s.unicodeScalars)
    let isArabic = u.contains { $0.value >= 0x0600 && $0.value <= 0x06FF }
    let isCJK = u.contains { ($0.value >= 0x4E00 && $0.value <= 0x9FFF)
                          || ($0.value >= 0x3040 && $0.value <= 0x30FF)
                          || ($0.value >= 0xAC00 && $0.value <= 0xD7AF) }
    let isCyr = u.contains { ($0.value >= 0x0400 && $0.value <= 0x04FF) }
    let candidates: [String]
    if isArabic {
        candidates = ["GeezaPro-Bold", "DamascusBold", "Baghdad", "Arial Unicode MS Bold"]
    } else if isCJK {
        candidates = ["PingFangSC-Semibold", "HiraginoSansGB-W6", "STHeiti-Medium", "Arial Unicode MS Bold"]
    } else if isCyr {
        candidates = ["Arial-BoldMT", "HelveticaNeue-Bold", "Arial Unicode MS Bold"]
    } else {
        candidates = ["Arial-BoldMT", "HelveticaNeue-Bold", "Arial Unicode MS Bold"]
    }
    for name in candidates {
        if let f = NSFont(name: name, size: size) { return f }
    }
    return NSFont.boldSystemFont(ofSize: size)
}

guard CommandLine.arguments.count >= 5 else {
    print("uso: card <salida.png> <indice> <total> <titulo>"); exit(1)
}
let outPath = CommandLine.arguments[1]
let idx = Int(CommandLine.arguments[2]) ?? 1
let total = Int(CommandLine.arguments[3]) ?? 8
let title = CommandLine.arguments[4]

let rep = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: Int(W), pixelsHigh: Int(H),
    bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false,
    colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0)!
NSGraphicsContext.saveGraphicsState()
NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: rep)
let ctx = NSGraphicsContext.current!.cgContext

let barH: CGFloat = 170
let top = CGFloat(H) - barH

// barra opaca (legibilidad sobre cualquier metraje)
ctx.setFillColor(NSColor(srgbRed: 6.0/255.0, green: 6.0/255.0, blue: 11.0/255.0, alpha: 0.95).cgColor)
ctx.fill(CGRect(x: 0, y: 0, width: W, height: barH))
// línea superior roja de acento
ctx.setFillColor(RED.cgColor)
ctx.fill(CGRect(x: 0, y: barH - 3, width: W, height: 3))
// lateral rojo
ctx.fill(CGRect(x: 0, y: 0, width: 10, height: barH))

// --- Numeración "SERVICIO 0X/08" ---
let numFont = NSFont(name: "Menlo-Bold", size: 21) ?? NSFont.boldSystemFont(ofSize: 21)
let num = "SERVICIO \(String(format: "%02d", idx))/\(String(format: "%02d", total))" as NSString
let numAttr: [NSAttributedString.Key: Any] = [.font: numFont, .foregroundColor: RED]
num.draw(at: NSPoint(x: 44, y: barH - 46), withAttributes: numAttr)

// --- Título: hasta 2 líneas, con CoreText para shaping/RTL ---
var size: CGFloat = 34
let maxW = CGFloat(W) - 100
var lines: [String] = [title]
func widthOf(_ s: String, _ f: NSFont) -> CGFloat {
    return (s as NSString).size(withAttributes: [.font: f]).width
}
if widthOf(title, fontFor(title, size: size)) > maxW {
    let words = title.split(separator: " ").map(String.init)
    if words.count > 1 {
        for i in 1..<words.count {
            let l1 = words[0..<i].joined(separator: " ")
            if widthOf(l1, fontFor(l1, size: size)) <= maxW {
                lines = [l1, words[i...].joined(separator: " ")]
                break
            }
        }
    }
    if lines.count == 1 {
        size = widthOf(title, fontFor(title, size: 30)) > maxW ? 24 : 30
    }
}
let tFont = fontFor(lines[0], size: size)
let titleAttr: [NSAttributedString.Key: Any] = [.font: tFont, .foregroundColor: NSColor.white]
for (i, ln) in lines.enumerated() {
    let f = fontFor(ln, size: size)
    var attrs: [NSAttributedString.Key: Any] = [.font: f, .foregroundColor: NSColor.white]
    if ln.unicodeScalars.contains(where: { $0.value >= 0x0600 && $0.value <= 0x06FF }) {
        attrs[.paragraphStyle] = NSParagraphStyle.default
    }
    (ln as NSString).draw(at: NSPoint(x: 44, y: barH - 104 - CGFloat(i) * (size + 8)), withAttributes: attrs)
}

NSGraphicsContext.restoreGraphicsState()
guard let data = rep.representation(using: .png, properties: [:]) else { exit(1) }
try data.write(to: URL(fileURLWithPath: outPath))
print("ok \(outPath)")
