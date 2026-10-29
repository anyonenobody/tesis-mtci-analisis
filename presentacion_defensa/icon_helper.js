/**
 * presentacion_defensa/icon_helper.js
 * ============================================================================
 * Renderizador de iconos vectoriales de React Icons (Fa, Hi, Md, etc.) a PNG
 * en formato Base64 para inserción de alta fidelidad en pptxgenjs.
 * Cumple estrictamente las directrices del skill `.agents/skills/pptx/SKILL.md`.
 * ============================================================================
 */

const React = require('react');
const ReactDOMServer = require('react-dom/server');
const sharp = require('sharp');

// Caché en memoria para evitar re-renderizados idénticos
const iconCache = new Map();

/**
 * Renderiza un componente de react-icons a PNG base64 listo para pptxgenjs.
 * @param {Function} IconComponent - Componente de react-icons (ej: FaLeaf, FaUniversity)
 * @param {string} colorHex - Color hex con o sin '#' (ej: '#1B365D' o '1B365D')
 * @param {number} size - Resolución de rasterizado (por defecto 256px para nitidez retina)
 * @returns {Promise<string>} String con prefijo 'image/png;base64,...'
 */
async function renderIconBase64(IconComponent, colorHex = '#1B365D', size = 256) {
  const safeColor = colorHex.startsWith('#') ? colorHex : `#${colorHex}`;
  const key = `${IconComponent.name || 'icon'}_${safeColor}_${size}`;

  if (iconCache.has(key)) {
    return iconCache.get(key);
  }

  const svg = ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComponent, { color: safeColor, size })
  );

  const pngBuffer = await sharp(Buffer.from(svg))
    .resize(size, size)
    .png()
    .toBuffer();

  const dataUri = `image/png;base64,${pngBuffer.toString('base64')}`;
  iconCache.set(key, dataUri);
  return dataUri;
}

module.exports = {
  renderIconBase64,
};

