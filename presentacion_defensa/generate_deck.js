/**
 * presentacion_defensa/generate_deck.js
 * ============================================================================
 * Generador Ejecutivo de la Presentación de Defensa de Tesis MTCI (UNAN-Managua)
 * Basado en pptxgenjs, React Icons y Sharp.
 * Cumple estrictamente con las directrices de .agents/skills/pptx/SKILL.md y CLAUDE.md
 * ============================================================================
 */

const path = require('path');
const fs = require('fs');
const pptxgen = require('pptxgenjs');
const { FaUniversity, FaBalanceScale, FaGraduationCap, FaBrain, FaLeaf, FaHandsHelping, FaBookOpen } = require('react-icons/fa');
const { renderIconBase64 } = require('./icon_helper');
const theme = require('./theme');

const OUTPUT_FILE = path.resolve(__dirname, '..', 'Presentacion_Defensa_Tesis_MTCI_UNAN.pptx');
const ASSETS_DIR = path.resolve(__dirname, '..', 'assets');
const APA7_DIR = path.join(ASSETS_DIR, 'figuras_apa7');
const DEF_ASSETS = path.join(__dirname, 'assets');

/**
 * Agrega el encabezado institucional estándar a una diapositiva.
 */
function addSlideHeader(slide, category, title) {
  // Categoría / Capítulo (Breadcrumb superior)
  slide.addText(category.toUpperCase(), {
    x: theme.layout.marginHeaderLeft,
    y: 0.45,
    w: 10.0,
    h: 0.3,
    fontSize: 10.5,
    bold: true,
    color: theme.colors.teal,
    fontFace: theme.fonts.header,
    margin: 0,
  });

  // Título de la diapositiva
  slide.addText(title, {
    x: theme.layout.marginHeaderLeft,
    y: 0.75,
    w: 11.0,
    h: 0.55,
    fontSize: 20,
    bold: true,
    color: theme.colors.navy,
    fontFace: theme.fonts.header,
    margin: 0,
  });

  // Línea divisoria decorativa sutil
  slide.addShape('line', {
    x: theme.layout.marginHeaderLeft,
    y: 1.35,
    w: 11.733,
    h: 0,
    line: { color: theme.colors.borderLight, width: 1.5 },
  });
}

async function buildDeck() {
  console.log('🚀 Iniciando construcción de la presentación de defensa MTCI...');
  const pres = new pptxgen();

  // 1. Configuración de dimensiones Widescreen 16:9
  pres.layout = 'LAYOUT_WIDE';
  pres.author = 'Dina Fabiola García Torres, Tatiana Paola López Ramos, Engel Enoc Zamora Velásquez';
  pres.company = 'UNAN-Managua CUR-Estelí';
  pres.title = 'Defensa de Tesis: MTCI en la Atención Psicológica';

  // ==========================================================================
  // SLIDE 01: PORTADA INSTITUCIONAL
  // ==========================================================================
  {
    const slide = pres.addSlide();
    slide.background = { color: theme.colors.navyDark };

    // Banda superior de acento
    slide.addShape('rect', {
      x: 0, y: 0, w: theme.layout.width, h: 0.15,
      fill: { color: theme.colors.teal },
      line: { color: theme.colors.teal }
    });

    // Logo / Escudo UNAN si existe
    const logoPath = path.join(ASSETS_DIR, 'extracted', 'unan_logo_clean.png');
    if (fs.existsSync(logoPath)) {
      slide.addImage({ path: logoPath, x: 0.8, y: 0.6, w: 1.4, h: 1.4 });
    }

    // Encabezado institucional
    slide.addText([
      { text: 'UNIVERSIDAD NACIONAL AUTÓNOMA DE NICARAGUA, MANAGUA\n', options: { fontSize: 13, bold: true, color: theme.colors.coral } },
      { text: 'UNAN-MANAGUA • CENTRO UNIVERSITARIO REGIONAL ESTELÍ (CUR-ESTELÍ)\n', options: { fontSize: 11, bold: false, color: 'D1D5DB' } },
      { text: 'DEPARTAMENTO DE CIENCIAS DE LA SALUD • CARRERA DE LICENCIATURA EN PSICOLOGÍA', options: { fontSize: 10, color: '9CA3AF' } }
    ], { x: 2.5, y: 0.65, w: 9.5, h: 1.3, margin: 0, fontFace: theme.fonts.header });

    // Título Principal de la Tesis
    slide.addText('La Medicina Tradicional, Complementaria e Integrativa (MTCI) como Complemento en la Atención Psicológica', {
      x: 0.8, y: 2.3, w: 11.7, h: 1.6,
      fontSize: 26, bold: true, color: theme.colors.bgWhite,
      fontFace: theme.fonts.header, margin: 0, lineSpacing: 34
    });

    // Subtítulo
    slide.addText('Estudio Mixto con Estudiantes, Facilitadores Locales y Docentes del CUR-Estelí (2026)', {
      x: 0.8, y: 3.9, w: 11.7, h: 0.6,
      fontSize: 16, color: theme.colors.sage,
      fontFace: theme.fonts.body, margin: 0
    });

    // Tarjeta inferior con Autores y Tutora
    slide.addShape('rect', {
      x: 0.8, y: 4.8, w: 11.733, h: 1.8,
      fill: { color: '142642' },
      line: { color: '1E3A5F', width: 1 }
    });

    slide.addText([
      { text: 'EQUIPO INVESTIGADOR (AUTORES):\n', options: { fontSize: 10, bold: true, color: theme.colors.coral } },
      { text: '• Dina Fabiola García Torres\n• Tatiana Paola López Ramos\n• Engel Enoc Zamora Velásquez', options: { fontSize: 12, color: theme.colors.bgWhite } }
    ], { x: 1.2, y: 5.0, w: 5.0, h: 1.4, margin: 0, fontFace: theme.fonts.body });

    slide.addText([
      { text: 'DOCENTE TUTORA:\n', options: { fontSize: 10, bold: true, color: theme.colors.coral } },
      { text: 'Dr. Tania Libertad Pérez Guevara\n\n', options: { fontSize: 12, bold: true, color: theme.colors.bgWhite } },
      { text: 'Estelí, Nicaragua • Segundo Semestre 2026', options: { fontSize: 10, color: '9CA3AF' } }
    ], { x: 6.8, y: 5.0, w: 5.2, h: 1.4, margin: 0, fontFace: theme.fonts.body });

    slide.addNotes(
      'INSTRUCCIÓN DE ORATORIA (Minuto 0:00 - 1:15):\n' +
      'Pausa inicial solemne. Saludar con respeto y formalidad a los Miembros del Honorable Tribunal Examinador.\n' +
      'Presentar a los tres autores y a la tutora. Señalar que esta investigación pionera en el CUR-Estelí ' +
      'articula la evidencia empírica en salud mental con la interculturalidad territorial de Las Segovias.'
    );
  }

  // ==========================================================================
  // SLIDE 02: PLANTEAMIENTO DEL PROBLEMA Y TENSIÓN JURÍDICA
  // ==========================================================================
  {
    const slide = pres.addSlide();
    slide.background = { color: theme.colors.bgCanvas };
    addSlideHeader(slide, 'Capítulo I • Planteamiento del Problema', 'Tensión Jurídica y Necesidad de Integración en Salud Mental');

    const iconLaw = await renderIconBase64(FaBalanceScale, '#1B365D', 256);
    const iconShield = await renderIconBase64(FaHandsHelping, '#2E86AB', 256);

    // Columna 1: Ley 774 (Derecho y Apertura)
    slide.addShape('rect', {
      x: 0.8, y: 1.6, w: 5.6, h: 4.8,
      fill: { color: theme.colors.bgWhite },
      line: { color: theme.colors.borderLight, width: 1 }
    });

    slide.addImage({ data: iconLaw, x: 1.2, y: 1.9, w: 0.6, h: 0.6 });
    slide.addText('LEY N.º 774: APERTURA Y DERECHO', {
      x: 2.0, y: 1.95, w: 4.0, h: 0.4,
      fontSize: 13, bold: true, color: theme.colors.navy, fontFace: theme.fonts.header, margin: 0
    });

    slide.addText([
      { text: '• Reconocimiento del derecho ciudadano a la medicina natural y terapias complementarias.\n\n', options: { bold: false } },
      { text: '• Integración promovida por el MINSA en el modelo MOSAFC institucional.\n\n', options: { bold: false } },
      { text: '• Alta demanda comunitaria en Estelí para manejo de estrés, duelo y ansiedad cotidiana.', options: { bold: false } }
    ], { x: 1.2, y: 2.7, w: 4.8, h: 3.2, fontSize: 13, color: theme.colors.textSecondary, fontFace: theme.fonts.body, margin: 0 });

    // Columna 2: Ley 292 (Límite y No Prescripción)
    slide.addShape('rect', {
      x: 6.9, y: 1.6, w: 5.6, h: 4.8,
      fill: { color: theme.colors.bgWhite },
      line: { color: theme.colors.borderLight, width: 1 }
    });

    slide.addImage({ data: iconShield, x: 7.3, y: 1.9, w: 0.6, h: 0.6 });
    slide.addText('LEY N.º 292: LÍMITE Y DELIMITACIÓN', {
      x: 8.1, y: 1.95, w: 4.0, h: 0.4,
      fontSize: 13, bold: true, color: theme.colors.coralDark, fontFace: theme.fonts.header, margin: 0
    });

    slide.addText([
      { text: '• Frontera legal estricta: Los profesionales de psicología NO poseen facultad de prescripción médica ni fitofarmacológica.\n\n', options: { bold: false } },
      { text: '• Fenómeno del Ocultamiento Terapéutico: Los usuarios ocultan sus prácticas etnobotánicas por temor al rechazo o juicio clínico.\n\n', options: { bold: false } },
      { text: '• Brecha Formativa: 100% de estudiantes y docentes señala ausencia de asignaturas dedicadas en la malla curricular.', options: { bold: false } }
    ], { x: 7.3, y: 2.7, w: 4.8, h: 3.2, fontSize: 13, color: theme.colors.textSecondary, fontFace: theme.fonts.body, margin: 0 });

    slide.addNotes(
      'INSTRUCCIÓN DE ORATORIA (Minuto 1:15 - 2:30):\n' +
      'Explicar con claridad la contradicción epistémica y legal: mientras la Ley 774 garantiza el acceso ciudadano a la MTCI, ' +
      'la Ley 292 fija el límite deontológico de que el psicólogo no prescribe. Esto genera el "ocultamiento terapéutico", ' +
      'donde el consultante utiliza plantas o rituales sin mencionarlo en psicoterapia. Subrayar la necesidad de formar ' +
      'psicólogos capaces de indagar y derivar éticamente.'
    );
  }

  // Guardar archivo
  await pres.writeFile({ fileName: OUTPUT_FILE });
  console.log(`✅ Presentación scaffold generada exitosamente en:\n   ${OUTPUT_FILE}`);
}

buildDeck().catch(err => {
  console.error('❌ Error construyendo la presentación:', err);
  process.exit(1);
});

