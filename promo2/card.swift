// Tarjeta de SERVICIO del promo (1280x720, RGBA) con CoreText:
//   card <salida.png> <etiqueta> <titulo>
//   etiqueta = "// SERVICIO 08"   titulo = "IA para tu comunicación"
//
// La tarjeta anuncia el SERVICIO (no el nombre del proyecto), con la misma
// tipografía display del sitio (Anton) para los alfabetos latinos y las
// fuentes del sistema para árabe/CJK/cirílico, que Anton no cubre.
// CoreText hace el shaping y el RTL que PIL/raqm no hacen en esta máquina.
import Foundation
import AppKit
import CoreText

let W: CGFloat = 1280, H: CGFloat = 720
let RED = NSColor(srgbRed: 1.0, green: 31.0/255.0, blue: 31.0/255.0, alpha: 1)
let ANTON = URL(fileURLWithPath: CommandLine.arguments.count > 4
    ? CommandLine.arguments[4]
    : "Anton-Regular.ttf")

// Anton (misma fuente que font-headline en el sitio)
var antonCGFont: CGFont?
if let data = try? Data(contentsOf: ANTON) as CFData,
   let provider = CGDataProvider(data: data) {
    if let f = CGFont(provider) {
        CTFontManagerRegisterGraphicsFont(f, nil)
        antonCGFont = f
    }
}

func scriptOf(_ s: String) -> String {
    let u = Array(s.unicodeScalars)
    if u.contains(where: { $0.value >= 0x0600 && $0.value <= 0x06FF }) { return "ar" }
    if u.contains(where: { ($0.value >= 0x4E00 && $0.value <= 0x9FFF)
                         || ($0.value >= 0x3040 && $0.value <= 0x30FF)
                         || ($0.value >= 0xAC00 && $0.value <= 0xD7AF) }) { return "cjk" }
    if u.contains(where: { $0.value >= 0x0400 && $0.value <= 0x04FF }) { return "cyr" }
    return "latin"
}

func fontFor(_ s: String, size: CGFloat) -> NSFont {
    let candidates: [String]
    switch scriptOf(s) {
    case "ar":   candidates = ["GeezaPro-Bold", "DamascusBold", "Arial Unicode MS Bold"]
    case "cjk":  candidates = ["PingFangSC-Semibold", "HiraginoSansGB-W6", "STHeiti-Medium",
                                "Arial Unicode MS Bold"]
    case "cyr":  candidates = ["Arial-BoldMT", "HelveticaNeue-Bold", "Arial Unicode MS Bold"]
    default:
        if let af = antonCGFont {
            return CTFontCreateWithGraphicsFont(af, size, nil, nil) as NSFont
        }
        candidates = ["Arial-BoldMT", "HelveticaNeue-Bold", "Arial Unicode MS Bold"]
    }
    for name in candidates {
        if let f = NSFont(name: name, size: size) { return f }
    }
    return NSFont.boldSystemFont(ofSize: size)
}

guard CommandLine.arguments.count >= 4 else {
    print("uso: card <salida.png> <etiqueta> <titulo> [anton.ttf]"); exit(1)
}
let outPath = CommandLine.arguments[1]
let label = CommandLine.arguments[2]
let title = CommandLine.arguments[3].uppercased()   // el sitio muestra los servicios en MAYÚSCULAS

let rep = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: Int(W), pixelsHigh: Int(H),
    bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false,
    colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0)!
NSGraphicsContext.saveGraphicsState()
NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: rep)
let ctx = NSGraphicsContext.current!.cgContext

// alto de la barra: los 80 títulos actuales caben en 1 línea a 46px; el bloque
// (etiqueta + hueco + título) se centra dentro con el mismo aire arriba y abajo.
// Si una traducción futura necesita 2 líneas, el bloque se encoge (ver abajo).
let barH: CGFloat = 156
let top = H - barH
let pad: CGFloat = 44

// fondo del velo: degradado hacia el negro para que la tarjeta funda con el metraje
let grad = CGGradient(colorsSpace: CGColorSpaceCreateDeviceRGB(),
    colors: [NSColor(srgbRed: 6.0/255.0, green: 6.0/255.0, blue: 11.0/255.0, alpha: 0).cgColor,
             NSColor(srgbRed: 6.0/255.0, green: 6.0/255.0, blue: 11.0/255.0, alpha: 0.96).cgColor]
    as CFArray, locations: [0.0, 0.35])!
ctx.saveGState()
ctx.clip(to: CGRect(x: 0, y: 0, width: W, height: barH + 60))
ctx.drawLinearGradient(grad, start: CGPoint(x: 0, y: barH + 60),
                       end: CGPoint(x: 0, y: 0), options: [])

// acento rojo en el borde superior
ctx.setFillColor(RED.cgColor)
ctx.fill(CGRect(x: 0, y: barH - 3, width: W, height: 3))
// rail lateral rojo
ctx.fill(CGRect(x: 0, y: 0, width: 10, height: barH))
ctx.restoreGState()

// --- Layout del texto por métricas de TINTA reales (CTLine), no por baselines
//     aproximadas: así la etiqueta y el título nunca se solapan ni se salen de
//     la barra en ningún idioma. El Y de CoreText crece hacia arriba, de modo
//     que `inkTopY` es la posición del BORDE SUPERIOR de la tinta y el bloque
//     se compone restando (hacia abajo).
func lineInk(_ s: String, font: NSFont) -> CGFloat {
    let line = CTLineCreateWithAttributedString(NSAttributedString(string: s, attributes: [
        .font: font]))
    return CGFloat(CTLineGetBoundsWithOptions(line, .useGlyphPathBounds).height)
}
func drawLine(_ s: String, font: NSFont, color: NSColor, inkTopY: CGFloat, x: CGFloat) {
    var attrs: [NSAttributedString.Key: Any] = [.font: font, .foregroundColor: color]
    if scriptOf(s) == "ar" { attrs[.paragraphStyle] = NSParagraphStyle.default }
    let line = CTLineCreateWithAttributedString(NSAttributedString(string: s, attributes: attrs))
    let ink = CTLineGetBoundsWithOptions(line, .useGlyphPathBounds)
    ctx.textPosition = CGPoint(x: x, y: inkTopY - CGFloat(ink.maxY))
    CTLineDraw(line, ctx)
}
func widthAt(_ s: String, _ size: CGFloat) -> CGFloat {
    let line = CTLineCreateWithAttributedString(NSAttributedString(string: s, attributes: [
        .font: fontFor(s, size: size)]))
    return CGFloat(CTLineGetTypographicBounds(line, nil, nil, nil))
}
func inkAt(_ s: String, _ size: CGFloat) -> CGFloat { lineInk(s, font: fontFor(s, size: size)) }

let GAP: CGFloat = 22                // aire entre la etiqueta y el título
let MARGIN: CGFloat = 24             // aire mínimo arriba y abajo del bloque
let LEAD: CGFloat = 0.26             // interlineado entre las 2 líneas del título
let maxW = W - pad * 2 - 24
let numFont = NSFont(name: "Menlo-Bold", size: 21) ?? NSFont.boldSystemFont(ofSize: 21)
let labelH = lineInk(label, font: numFont)

// 1) cuerpo del título: el mayor que quepa en 1 línea; si no, en 2
var size: CGFloat = 46
var lines: [String] = [title]
let avail = barH - MARGIN * 2 - labelH - GAP     // alto para el título
while size > 30 && widthAt(title, size) > maxW { size -= 2 }   // 1 línea hasta 30px
if widthAt(title, size) > maxW {
    let words = title.split(separator: " ", omittingEmptySubsequences: false).map(String.init)
    if words.count > 1 {
        for i in 1..<words.count {
            let l1 = words[0..<i].joined(separator: " ")
            if widthAt(l1, size) <= maxW { lines = [l1, words[i...].joined(separator: " ")]; break }
        }
    }
    if lines.count == 1 {                       // sin espacios (CJK): corte por caracteres
        let chars = Array(title)
        let half = max(1, chars.count / 2)
        lines = [String(chars[0..<half]), String(chars[half...])]
    }
    while size > 18 {                           // que las 2 líneas quepan en alto y ancho
        let h = max(inkAt(lines[0], size), inkAt(lines[1], size))
        if inkAt(lines[0], size) + h * LEAD + inkAt(lines[1], size) <= avail
            && widthAt(lines[0], size) <= maxW && widthAt(lines[1], size) <= maxW { break }
        size -= 2
    }
}

// 2) centro vertical el bloque (etiqueta + hueco + título) dentro de la barra
let titleHs = lines.map { inkAt($0, size) }
let titleBlock = titleHs.reduce(0, +) + LEAD * max(titleHs[0], titleHs.last ?? 0)
    * CGFloat(max(0, lines.count - 1))
let block = labelH + GAP + titleBlock
let blockTop = barH - max(MARGIN, (barH - block) / 2)

drawLine(label, font: numFont, color: RED, inkTopY: blockTop, x: pad)
var y = blockTop - labelH - GAP
for (i, ln) in lines.enumerated() {
    drawLine(ln, font: fontFor(ln, size: size), color: NSColor.white, inkTopY: y, x: pad)
    y -= titleHs[i] + (i < lines.count - 1 ? LEAD * max(titleHs[i], titleHs[i + 1]) : 0)
}

NSGraphicsContext.restoreGraphicsState()
guard let data = rep.representation(using: .png, properties: [:]) else { exit(1) }
try data.write(to: URL(fileURLWithPath: outPath))
