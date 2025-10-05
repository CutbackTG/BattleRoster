// characters.js - Google Sheets Integration

const API_KEY = '14ProN3lR8p-t9j2P7b76JBOwEIrvntHqCVBee1q6bNk';

// Your Google Sheet ID (from the URL of your sheet)
const SHEET_ID = '1371778561';

const WORKSHEETS = {
  characterInfo: 'Character Info',
  abilities: 'Abilities',
  combat: 'Combat',
  skills: 'Skills & Saves',
  equipment: 'Equipment',
  features: 'Features & Traits',
  spells: 'Spells',
  notes: 'Notes & Personality'
};

// GOOGLE SHEETS API FUNCTIONS

/**
 * Fetch data from a specific worksheet
 * @param {string} sheetName - Name of the worksheet tab
 * @param {string} range - Cell range (e.g., 'A1:Z100')
 * @returns {Promise<Array>} - Array of rows
 */
async function fetchSheetData(sheetName, range = '') {
  const fullRange = range ? `${sheetName}!${range}` : sheetName;
  const url = `https://sheets.googleapis.com/v4/spreadsheets/${SHEET_ID}/values/${fullRange}?key=${API_KEY}`;
  
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data.values || [];
  } catch (error) {
    console.error(`Error fetching sheet "${sheetName}":`, error);
    return [];
  }
}

/**
 * Convert sheet rows to object using first row as keys
 * @param {Array} rows - Array of rows from Google Sheets
 * @returns {Object} - Object with key-value pairs
 */
function rowsToObject(rows) {
  if (rows.length < 2) return {};
  
  const headers = rows[0];
  const values = rows[1];
  const obj = {};
  
  headers.forEach((header, index) => {
    obj[header] = values[index] || '';
  });
  
  return obj;
}

/**
 * Load complete character data from all worksheets
 * @returns {Promise<Object>} - Complete character object
 */
async function loadCharacterFromSheets() {
  try {
    console.log('Loading character data from Google Sheets...');
    
    // Fetch all worksheets in parallel
    const [
      characterInfoData,
      abilitiesData,
      combatData,
      skillsData,
      equipmentData,
      featuresData,
      spellsData,
      notesData
    ] = await Promise.all([
      fetchSheetData(WORKSHEETS.characterInfo, 'A1:B20'),
      fetchSheetData(WORKSHEETS.abilities, 'A1:B10'),
      fetchSheetData(WORKSHEETS.combat, 'A1:D10'),
      fetchSheetData(WORKSHEETS.skills, 'A1:B30'),
      fetchSheetData(WORKSHEETS.equipment, 'A1:D20'),
      fetchSheetData(WORKSHEETS.features, 'A1:B10'),
      fetchSheetData(WORKSHEETS.spells, 'A1:C50'),
      fetchSheetData(WORKSHEETS.notes, 'A1:B10')
    ]);
    
    // Convert to objects
    const characterInfo = rowsToObject(characterInfoData);
    const abilities = rowsToObject(abilitiesData);
    const notes = rowsToObject(notesData);
    
    // Parse weapons from equipment (assuming columns: Name, Attack Bonus, Damage)
    const weapons = equipmentData.slice(1).map(row => ({
      name: row[0] || '',
      attack_bonus: row[1] || '+0',
      damage: row[2] || '1d6'
    })).filter(weapon => weapon.name);
    
    // Parse spells (assuming columns: Level, Name, Description)
    const cantrips = spellsData
      .slice(1)
      .filter(row => row[0] === '0' || row[0] === 'Cantrip')
      .map(row => row[1])
      .filter(spell => spell);
    
    // Parse skills (assuming columns: Skill, Modifier)
    const skills = {};
    skillsData.slice(1).forEach(row => {
      if (row[0]) {
        skills[row[0].toLowerCase()] = row[1] || '+0';
      }
    });
    
    // Build complete character object
    const character = {
      name: characterInfo['Character Name'] || 'Unknown Character',
      race: characterInfo['Race'] || '',
      class: characterInfo['Class'] || '',
      level: characterInfo['Level'] || '1',
      
      // Abilities
      strength: abilities['Strength'] || '10',
      str_mod: calculateModifier(abilities['Strength']),
      dexterity: abilities['Dexterity'] || '10',
      dex_mod: calculateModifier(abilities['Dexterity']),
      constitution: abilities['Constitution'] || '10',
      con_mod: calculateModifier(abilities['Constitution']),
      intelligence: abilities['Intelligence'] || '10',
      int_mod: calculateModifier(abilities['Intelligence']),
      wisdom: abilities['Wisdom'] || '10',
      wis_mod: calculateModifier(abilities['Wisdom']),
      charisma: abilities['Charisma'] || '10',
      cha_mod: calculateModifier(abilities['Charisma']),
      
      // Skills
      stealth: skills['stealth'] || '+0',
      arcana: skills['arcana'] || '+0',
      
      // Equipment
      weapons: weapons,
      
      // Spells
      spells: {
        cantrips: cantrips
      },
      
      // Personality
      personality: notes['Personality'] || '',
      ideals: notes['Ideals'] || '',
      bonds: notes['Bonds'] || '',
      flaws: notes['Flaws'] || ''
    };
    
    console.log('Character data loaded successfully:', character);
    return character;
    
  } catch (error) {
    console.error('Error loading character from sheets:', error);
    return null;
  }
}

/**
 * Calculate ability modifier from score
 * @param {string|number} score - Ability score
 * @returns {number} - Modifier value
 */
function calculateModifier(score) {
  const numScore = parseInt(score) || 10;
  return Math.floor((numScore - 10) / 2);
}

// ==========================================
// UI UPDATE FUNCTIONS
// ==========================================

/**
 * Update the character sheet UI with character data
 * @param {Object} character - Character data object
 */
function updateCharacterSheet(character) {
  if (!character) {
    console.error('No character data to display');
    return;
  }
  
  // Update character name
  const nameElement = document.querySelector('.character-sheet h1');
  if (nameElement) {
    nameElement.textContent = character.name;
  }
  
  // Update ability scores
  const abilities = [
    { index: 0, score: character.strength, mod: character.str_mod },
    { index: 1, score: character.dexterity, mod: character.dex_mod },
    { index: 2, score: character.constitution, mod: character.con_mod },
    { index: 3, score: character.intelligence, mod: character.int_mod },
    { index: 4, score: character.wisdom, mod: character.wis_mod },
    { index: 5, score: character.charisma, mod: character.cha_mod }
  ];
  
  const abilityElements = document.querySelectorAll('.ability');
  abilities.forEach(ability => {
    if (abilityElements[ability.index]) {
      const scoreEl = abilityElements[ability.index].querySelector('.score');
      const modEl = abilityElements[ability.index].querySelector('.modifier');
      
      if (scoreEl) scoreEl.textContent = ability.score;
      if (modEl) modEl.textContent = ability.mod >= 0 ? `+${ability.mod}` : `${ability.mod}`;
    }
  });
  
  // Update skills
  const skillsList = document.querySelector('.skills ul');
  if (skillsList) {
    skillsList.innerHTML = `
      <li>Stealth: ${character.stealth}</li>
      <li>Arcana: ${character.arcana}</li>
    `;
  }
  
  // Update weapons table
  const weaponsTableBody = document.querySelector('.weapons table tbody');
  if (weaponsTableBody && character.weapons.length > 0) {
    weaponsTableBody.innerHTML = '';
    character.weapons.forEach(weapon => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${weapon.name}</td>
        <td>${weapon.attack_bonus}</td>
        <td>${weapon.damage}</td>
      `;
      weaponsTableBody.appendChild(row);
    });
  }
  
  // Update spells
  const spellsList = document.querySelector('.spells ul');
  if (spellsList && character.spells.cantrips.length > 0) {
    spellsList.innerHTML = '';
    character.spells.cantrips.forEach(spell => {
      const li = document.createElement('li');
      li.textContent = spell;
      spellsList.appendChild(li);
    });
  }
  
  // Update traits
  const traitsDiv = document.querySelector('.traits');
  if (traitsDiv) {
    traitsDiv.innerHTML = `
      <h3>Traits</h3>
      <p><strong>Personality:</strong> ${character.personality}</p>
      <p><strong>Ideals:</strong> ${character.ideals}</p>
      <p><strong>Bonds:</strong> ${character.bonds}</p>
      <p><strong>Flaws:</strong> ${character.flaws}</p>
    `;
  }
  
  console.log('Character sheet updated successfully ✅');
}

/**
 * Show loading state
 */
function showLoading() {
  const nameElement = document.querySelector('.character-sheet h1');
  if (nameElement) {
    nameElement.textContent = 'Loading character data...';
  }
}

/**
 * Show error message
 */
function showError(message) {
  const nameElement = document.querySelector('.character-sheet h1');
  if (nameElement) {
    nameElement.textContent = 'Error loading character';
    nameElement.style.color = '#c00';
  }
  alert(`Error: ${message}\n\nPlease check:\n1. Your API key is correct\n2. Your Sheet ID is correct\n3. The sheet is publicly accessible\n4. Check the browser console for details`);
}


/**
 * Initialize the character sheet when page loads
 */
async function initializeCharacterSheet() {
  // Validate configuration
  if (API_KEY === 'YOUR_API_KEY_HERE' || SHEET_ID === 'YOUR_SHEET_ID_HERE') {
    console.error('⚠️ Please update API_KEY and SHEET_ID in characters.js');
    showError('Configuration missing. Please update API_KEY and SHEET_ID in characters.js');
    return;
  }
  
  showLoading();
  
  try {
    const character = await loadCharacterFromSheets();
    
    if (character) {
      updateCharacterSheet(character);
    } else {
      showError('Failed to load character data. Check console for details.');
    }
  } catch (error) {
    console.error('Initialization error:', error);
    showError(error.message);
  }
}

// Load character data when page loads
document.addEventListener('DOMContentLoaded', initializeCharacterSheet);