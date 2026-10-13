export const categorias = [
  {
    nombre: "Liga Española",
    temporada: "2026/27",
    slug: "liga-espanola",
    logo: "/images/ligas/laliga.png",
    equipos: [
      "UD Almería", "Athletic Club", "Atlético de Madrid", "CA Osasuna",
      "Celta", "Deportivo Alavés", "RCD Espanyol", "FC Barcelona", "Getafe CF", "Girona FC",
      "RC Deportivo", "CD Leganés", "Levante UD", "Málaga CF",
      "RCD Mallorca", "Racing de Santander", "Rayo Vallecano", "Real Betis",
      "Real Madrid", "Real Oviedo", "Real Sociedad", "Real Valladolid CF",
      "Real Zaragoza", "Sevilla FC", "Valencia CF", "Villarreal CF"
    ]
  },
  {
    nombre: "Liga Inglesa",
    temporada: "2026/27",
    slug: "liga-inglesa",
    logo: "/images/ligas/premier-league.png",
    equipos: [
      "Arsenal", "Aston Villa", "Chelsea", "Crystal Palace", "Everton",
      "Leicester City", "Liverpool", "Manchester City", "Manchester United",
      "Newcastle United", "Tottenham Hotspur", "West Ham United"
    ]
  },
  {
    nombre: "Liga Italiana",
    temporada: "2026/27",
    slug: "liga-italiana",
    logo: "/images/ligas/serie-a.png",
    equipos: [
      "AC Milan", "Roma", "Atalanta", "Como", "Fiorentina", "Inter",
      "Juventus", "Lazio", "Napoli", "Parma", "Sassuolo"
    ]
  },
  {
    nombre: "Liga Francesa",
    temporada: "2026/27",
    slug: "liga-francesa",
    logo: "/images/ligas/ligue-1.png",
    equipos: [
      "OGC Nice", "Olympique Lyonnais", "Olympique de Marseille",
      "Paris Saint-Germain"
    ]
  },
  {
    nombre: "Liga Alemana",
    temporada: "2026/27",
    slug: "liga-alemana",
    logo: "/images/ligas/bundesliga.png",
    equipos: [
      "Bayer Leverkusen", "Bayern Munich", "Borussia Dortmund",
      "Borussia Mönchengladbach", "Eintracht Frankfurt", "Union Berlin",
      "RB Leipzig", "Schalke 04", "Werder Bremen", "VfL Wolfsburg"
    ]
  },
  {
    nombre: "Selecciones",
    temporada: "2026",
    slug: "selecciones",
    logo: "/images/ligas/selecciones.png",
    equipos: [
      "Alemania", "Argentina", "Bélgica", "Brasil", "Colombia", "Croacia", "Curazao", "España", "Estados Unidos",
      "Francia", "Inglaterra", "Italia", "Japón", "Marruecos",
      "México", "Noruega", "Países Bajos", "Perú", "Portugal", "Uruguay"
    ]
  }
];

export function crearSlug(texto: string) {
  return texto
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/&/g, "and")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

export function obtenerEscudo(equipo: string) {
  return `/images/equipos/${crearSlug(equipo)}.png`;
}
