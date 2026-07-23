export const categorias = [
  {
  nombre: "Liga Española",
  slug: "liga-espanola",
  logo: "/images/ligas/laliga.png",
  equipos: [
    "Athletic Club",
    "Atlético de Madrid",
    "CA Osasuna",
    "Celta",
    "Deportivo Alavés",
    "Elche CF",
    "FC Barcelona",
    "Getafe CF",
    "Levante UD",
    "Málaga CF",
    "Racing de Santander",
    "Rayo Vallecano",
    "RC Deportivo",
    "RCD Espanyol",
    "Real Betis",
    "Real Madrid",
    "Real Sociedad",
    "Sevilla FC",
    "Valencia CF",
    "Villarreal CF",

    "AD Ceuta FC",
    "Albacete BP",
    "Burgos CF",
    "Cádiz CF",
    "CD Castellón",
    "CD Eldense",
    "CD Leganés",
    "CD Tenerife",
    "CE Sabadell",
    "Celta Fortuna",
    "Córdoba CF",
    "FC Andorra",
    "Girona FC",
    "Granada CF",
    "Real Sociedad B",
    "RCD Mallorca",
    "Real Oviedo",
    "Real Sporting",
    "Real Valladolid CF",
    "SD Eibar",
    "UD Almería",
    "UD Las Palmas"
  ]
},

  {
    nombre: "Liga Inglesa",
    temporada: "2026/27",
    slug: "liga-inglesa",
    logo: "/images/ligas/premier-league.png",
    equipos: [
      "Arsenal",
      "Aston Villa",
      "Bournemouth",
      "Brentford",
      "Brighton & Hove Albion",
      "Chelsea",
      "Coventry City",
      "Everton",
      "Hull City",
      "Ipswich Town",
      "Leeds United",
      "Liverpool",
      "Manchester City",
      "Manchester United",
      "Newcastle United",
      "Nottingham Forest",
      "Sunderland",
      "Tottenham Hotspur",
      "West Ham United",
      "Wolverhampton Wanderers"
    ]
  },

  {
    nombre: "Liga Italiana",
    temporada: "2026/27",
    slug: "liga-italiana",
    logo: "/images/ligas/serie-a.png",
    equipos: [
      "AC Milan",
      "Atalanta",
      "Bologna",
      "Cagliari",
      "Como",
      "Fiorentina",
      "Frosinone",
      "Genoa",
      "Inter",
      "Juventus",
      "Lazio",
      "Lecce",
      "Monza",
      "Napoli",
      "Parma",
      "Roma",
      "Sassuolo",
      "Torino",
      "Udinese",
      "Venezia"
    ]
  },

  {
    nombre: "Liga Francesa",
    temporada: "2026/27",
    slug: "liga-francesa",
    logo: "/images/ligas/ligue-1.png",
    equipos: [
      "Angers SCO",
      "AJ Auxerre",
      "AS Monaco",
      "Stade Brestois",
      "FC Lorient",
      "Le Havre AC",
      "LOSC Lille",
      "OGC Nice",
      "Olympique Lyonnais",
      "Olympique de Marseille",
      "Paris FC",
      "Paris Saint-Germain",
      "RC Lens",
      "Stade Rennais",
      "RC Strasbourg",
      "Toulouse FC",
      "Le Mans FC",
      "ESTAC Troyes"
    ]
  },

  {
    nombre: "Liga Alemana",
    temporada: "2026/27",
    slug: "liga-alemana",
    logo: "/images/ligas/bundesliga.png",
    equipos: [
      "Bayern Munich",
      "Borussia Dortmund",
      "RB Leipzig",
      "VfB Stuttgart",
      "TSG Hoffenheim",
      "Bayer Leverkusen",
      "SC Freiburg",
      "Eintracht Frankfurt",
      "FC Augsburg",
      "Mainz 05",
      "Union Berlin",
      "Borussia Mönchengladbach",
      "Hamburger SV",
      "FC Köln",
      "Werder Bremen",
      "Schalke 04",
      "SV Elversberg",
      "SC Paderborn"
    ]
  },

  {
    nombre: "Selecciones",
    temporada: "2026",
    slug: "selecciones",
    logo: "/images/ligas/selecciones.png",
    equipos: [
      "Alemania",
      "Argentina",
      "Bélgica",
      "Brasil",
      "Colombia",
      "Croacia",
      "Ecuador",
      "España",
      "Estados Unidos",
      "Francia",
      "Inglaterra",
      "Italia",
      "Japón",
      "Marruecos",
      "México",
      "Países Bajos",
      "Portugal",
      "Senegal",
      "Uruguay"
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