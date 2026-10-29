/**
 * presentacion_defensa/theme.js
 * ============================================================================
 * Constantes de Diseño y Paleta Institucional UNAN-Managua / MTCI para pptxgenjs.
 * REGLA ESTRICTA DE PPTXGENJS: Códigos hexadecimales SIEMPRE de 6 dígitos SIN '#'
 * ============================================================================
 */

module.exports = {
  // Paleta de Colores Oficial (SIN '#')
  colors: {
    // Azul Institucional UNAN-Managua (Autoridad, rigor académico)
    navy: '1B365D',
    navyDark: '0F2038',
    navyLight: '2D4E7B',

    // Verde Salvia Etnobotánico (Plantas medicinales, naturaleza, integración)
    sage: '6B8F7A',
    sageDark: '4C6A5A',
    sageLight: 'EBF3EE',

    // Azul Clínico / Empírico (Salud mental, psicología aplicada)
    teal: '2E86AB',
    tealDark: '1E5F7A',
    tealLight: 'E1EFF5',

    // Naranja / Ámbar Cálido (Alertas normativas, paradojas, acentos)
    coral: 'E6955F',
    coralDark: 'C47038',
    coralLight: 'FDF2EB',

    // Neutros Tipográficos y Fondos
    textPrimary: '1F2937',     // Slate 800
    textSecondary: '4B5563',   // Slate 600
    textMuted: '6B7280',       // Slate 500
    textLight: '9CA3AF',       // Slate 400

    bgCanvas: 'F8F9FA',        // Blanco roto limpio
    bgWhite: 'FFFFFF',         // Blanco puro
    bgCard: 'FFFFFF',
    bgDark: '0F2038',          // Para diapositivas de impacto oscuro
    borderLight: 'E5E7EB',     // Gris sutil para separadores
    borderAccent: 'D1D5DB',
  },

  // Tipografías Seguras del Sistema
  fonts: {
    header: 'Arial',
    body: 'Calibri',
    metric: 'Arial',
  },

  // Dimensiones en Pulgadas para Widescreen 16:9 (LAYOUT_WIDE: 13.333" x 7.5")
  layout: {
    name: 'LAYOUT_WIDE',
    width: 13.333,
    height: 7.5,
    marginHeaderTop: 0.5,
    marginHeaderLeft: 0.8,
    contentTop: 1.5,
    contentBottom: 6.8,
    contentLeft: 0.8,
    contentRight: 12.533,
  },
};
