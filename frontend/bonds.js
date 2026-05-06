// ============================================
//  BOND CENTRAL — Bonds Page JS
// ============================================

let allBonds = window.BONDS_DATA || [];
let filteredBonds = [...allBonds];
let currentPage = 1;
const PER_PAGE = 8;

function getRatingBadge(rating) {
  const cls = rating === 'AAA' ? 'rating-aaa' : rating === 'AA+' || rating === 'AA' ? 'rating-aa' : 'rating-a';
  return `<span class="rating-badge ${cls}">${rating}</span>`;
}

function renderBonds() {
  const tbody = document.getElementById('bonds-tbody');
  if (!tbody) return;
  const start = (currentPage - 1) * PER_PAGE;
  const pageBonds = filteredBonds.slice(start, start + PER_PAGE);

  if (pageBonds.length === 0) {
    tbody.innerHTML = `<tr><td colspan="7" style="text-align:center;padding:3rem;color:var(--text-muted);">No bonds found matching your criteria.</td></tr>`;
    return;
  }

  tbody.innerHTML = pageBonds.map(b => `
    <tr>
      <td>
        <div class="bond-issuer">${b.issuer}</div>
        <div style="font-size:0.75rem;color:var(--text-muted);margin-top:2px;">ISIN: ${b.isin} · ${b.exchange}</div>
      </td>
      <td>${b.type}</td>
      <td>${getRatingBadge(b.rating)}</td>
      <td class="yield-val">${b.yield.toFixed(2)}%</td>
      <td>${b.maturity}</td>
      <td>₹${b.minInvest.toLocaleString('en-IN')}</td>
      <td><button class="invest-btn" onclick="viewBond(${b.id})">Invest →</button></td>
    </tr>
  `).join('');

  renderPagination();
}

function renderPagination() {
  const pg = document.getElementById('pagination');
  if (!pg) return;
  const totalPages = Math.ceil(filteredBonds.length / PER_PAGE);
  let html = '';
  for (let i = 1; i <= totalPages; i++) {
    html += `<button onclick="goToPage(${i})" style="padding:0.4rem 0.8rem;border-radius:6px;border:1px solid var(--border);background:${i===currentPage ? 'var(--gold)' : 'transparent'};color:${i===currentPage ? 'var(--navy)' : 'var(--text-muted)'};cursor:pointer;font-family:'DM Sans',sans-serif;">${i}</button>`;
  }
  pg.innerHTML = html;
}

function goToPage(p) {
  currentPage = p;
  renderBonds();
  window.scrollTo({ top: 200, behavior: 'smooth' });
}

function filterBonds() {
  const q = (document.getElementById('bond-search')?.value || '').toLowerCase();
  filteredBonds = allBonds.filter(b =>
    b.issuer.toLowerCase().includes(q) ||
    b.type.toLowerCase().includes(q) ||
    b.isin.toLowerCase().includes(q) ||
    b.rating.toLowerCase().includes(q)
  );
  currentPage = 1;
  renderBonds();
}

function sortBonds(val) {
  if (val === 'yield-desc') filteredBonds.sort((a,b) => b.yield - a.yield);
  else if (val === 'yield-asc') filteredBonds.sort((a,b) => a.yield - b.yield);
  else if (val === 'rating') filteredBonds.sort((a,b) => a.rating.localeCompare(b.rating));
  else if (val === 'maturity') filteredBonds.sort((a,b) => new Date(a.maturity) - new Date(b.maturity));
  renderBonds();
}

function applyFilters() {
  const q = (document.getElementById('bond-search')?.value || '').toLowerCase();
  const maxYield = +document.getElementById('yield-range')?.value || 15;

  const checkedTypes = [];
  if (document.getElementById('gov')?.checked) checkedTypes.push('G-Sec');
  if (document.getElementById('corp')?.checked) checkedTypes.push('Corporate');
  if (document.getElementById('psu')?.checked) checkedTypes.push('PSU');
  if (document.getElementById('sgb')?.checked) checkedTypes.push('SGB');
  if (document.getElementById('zero')?.checked) checkedTypes.push('Zero Coupon');
  if (document.getElementById('ec54')?.checked) checkedTypes.push('54EC');

  filteredBonds = allBonds.filter(b => {
    const matchType = checkedTypes.length === 0 || checkedTypes.includes(b.type);
    const matchYield = b.yield <= maxYield;
    const matchSearch = !q || b.issuer.toLowerCase().includes(q) || b.type.toLowerCase().includes(q);
    return matchType && matchYield && matchSearch;
  });
  currentPage = 1;
  renderBonds();
}

function viewBond(id) {
  const bond = allBonds.find(b => b.id === id);
  if (!bond) return;
  alert(`Bond Details:\n\nIssuer: ${bond.issuer}\nType: ${bond.type}\nRating: ${bond.rating}\nYield: ${bond.yield}% p.a.\nMaturity: ${bond.maturity}\nMin. Investment: ₹${bond.minInvest.toLocaleString('en-IN')}\nISIN: ${bond.isin}\nExchange: ${bond.exchange}\n\nLogin to invest in this bond.`);
}

// Check URL params for pre-filtering
function checkURLParams() {
  const params = new URLSearchParams(window.location.search);
  const type = params.get('type');
  if (type) {
    const typeMap = { government:'G-Sec', corporate:'Corporate', psu:'PSU', sgb:'SGB', zerocoupon:'Zero Coupon', '54ec':'54EC' };
    const mapped = typeMap[type];
    if (mapped) {
      filteredBonds = allBonds.filter(b => b.type === mapped);
    }
  }
}

// Init
checkURLParams();
renderBonds();
