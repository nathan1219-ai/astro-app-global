export const SIGN_LOCAL: Record<string, Record<string, string>> = {
  '白羊座': { en: 'Aries', es: 'Aries', fr: 'Bélier', de: 'Widder', it: 'Ariete', pt: 'Áries', ru: 'Овен' },
  '金牛座': { en: 'Taurus', es: 'Tauro', fr: 'Taureau', de: 'Stier', it: 'Toro', pt: 'Touro', ru: 'Телец' },
  '双子座': { en: 'Gemini', es: 'Géminis', fr: 'Gémeaux', de: 'Zwillinge', it: 'Gemelli', pt: 'Gêmeos', ru: 'Близнецы' },
  '巨蟹座': { en: 'Cancer', es: 'Cáncer', fr: 'Cancer', de: 'Krebs', it: 'Cancro', pt: 'Câncer', ru: 'Рак' },
  '狮子座': { en: 'Leo', es: 'Leo', fr: 'Lion', de: 'Löwe', it: 'Leone', pt: 'Leão', ru: 'Лев' },
  '处女座': { en: 'Virgo', es: 'Virgo', fr: 'Vierge', de: 'Jungfrau', it: 'Vergine', pt: 'Virgem', ru: 'Дева' },
  '天秤座': { en: 'Libra', es: 'Libra', fr: 'Balance', de: 'Waage', it: 'Bilancia', pt: 'Libra', ru: 'Весы' },
  '天蝎座': { en: 'Scorpio', es: 'Escorpio', fr: 'Scorpion', de: 'Skorpion', it: 'Scorpione', pt: 'Escorpião', ru: 'Скорпион' },
  '射手座': { en: 'Sagittarius', es: 'Sagitario', fr: 'Sagittaire', de: 'Schütze', it: 'Sagittario', pt: 'Sagitário', ru: 'Стрелец' },
  '摩羯座': { en: 'Capricorn', es: 'Capricornio', fr: 'Capricorne', de: 'Steinbock', it: 'Capricorno', pt: 'Capricórnio', ru: 'Козерог' },
  '水瓶座': { en: 'Aquarius', es: 'Acuario', fr: 'Verseau', de: 'Wassermann', it: 'Acquario', pt: 'Aquário', ru: 'Водолей' },
  '双鱼座': { en: 'Pisces', es: 'Piscis', fr: 'Poissons', de: 'Fische', it: 'Pesci', pt: 'Peixes', ru: 'Рыбы' }
}

export const ZODIAC_LOCAL: Record<string, Record<string, string>> = {
  '鼠': { en: 'Rat', es: 'Rata', fr: 'Rat', de: 'Ratte', it: 'Topo', pt: 'Rato', ru: 'Крыса' },
  '牛': { en: 'Ox', es: 'Buey', fr: 'Bœuf', de: 'Ochse', it: 'Bue', pt: 'Boi', ru: 'Бык' },
  '虎': { en: 'Tiger', es: 'Tigre', fr: 'Tigre', de: 'Tiger', it: 'Tigre', pt: 'Tigre', ru: 'Тигр' },
  '兔': { en: 'Rabbit', es: 'Conejo', fr: 'Lapin', de: 'Hase', it: 'Coniglio', pt: 'Coelho', ru: 'Кролик' },
  '龙': { en: 'Dragon', es: 'Dragón', fr: 'Dragon', de: 'Drache', it: 'Drago', pt: 'Dragão', ru: 'Дракон' },
  '蛇': { en: 'Snake', es: 'Serpiente', fr: 'Serpent', de: 'Schlange', it: 'Serpente', pt: 'Serpente', ru: 'Змея' },
  '马': { en: 'Horse', es: 'Caballo', fr: 'Cheval', de: 'Pferd', it: 'Cavallo', pt: 'Cavalo', ru: 'Лошадь' },
  '羊': { en: 'Goat', es: 'Cabra', fr: 'Chèvre', de: 'Ziege', it: 'Capra', pt: 'Cabra', ru: 'Коза' },
  '猴': { en: 'Monkey', es: 'Mono', fr: 'Singe', de: 'Affe', it: 'Scimmia', pt: 'Macaco', ru: 'Обезьяна' },
  '鸡': { en: 'Rooster', es: 'Gallo', fr: 'Coq', de: 'Hahn', it: 'Gallo', pt: 'Galo', ru: 'Петух' },
  '狗': { en: 'Dog', es: 'Perro', fr: 'Chien', de: 'Hund', it: 'Cane', pt: 'Cão', ru: 'Собака' },
  '猪': { en: 'Pig', es: 'Cerdo', fr: 'Cochon', de: 'Schwein', it: 'Maiale', pt: 'Porco', ru: 'Свинья' }
}

export const ELEMENT_LOCAL: Record<string, Record<string,string>> = {
  '木': { en: 'Wood', es: 'Madera', fr: 'Bois', de: 'Holz', it: 'Legno', pt: 'Madeira', ru: 'Древесная' },
  '火': { en: 'Fire', es: 'Fuego', fr: 'Feu', de: 'Feuer', it: 'Fuoco', pt: 'Fogo', ru: 'Огненная' },
  '土': { en: 'Earth', es: 'Tierra', fr: 'Terre', de: 'Erde', it: 'Terra', pt: 'Terra', ru: 'Земная' },
  '金': { en: 'Metal', es: 'Metal', fr: 'Métal', de: 'Metall', it: 'Metallo', pt: 'Metal', ru: 'Металлическая' },
  '水': { en: 'Water', es: 'Agua', fr: 'Eau', de: 'Wasser', it: 'Acqua', pt: 'Água', ru: 'Водная' }
}

export function chooseLocale(base: string, nav?: string): string {
  const n = nav || (typeof navigator !== 'undefined' ? navigator.language : '')
  if (base === 'pt') return n.startsWith('pt') && n.includes('BR') ? 'pt-BR' : 'pt-PT'
  if (base === 'es') return 'es-ES'
  if (base === 'fr') return 'fr-FR'
  if (base === 'de') return 'de-DE'
  if (base === 'it') return 'it-IT'
  if (base === 'ru') return 'ru-RU'
  return 'en-US'
}

export function resolveLocal(map: Record<string, Record<string,string>>, term: string, locale: string, base: string): string {
  const entry = map[term]
  if (!entry) return term
  return entry[locale] ?? entry[base] ?? entry['en'] ?? term
}
