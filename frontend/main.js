// ============================================
//  BOND CENTRAL — Main JavaScript
// ============================================

// --- Mobile Menu ---
function toggleMenu() {
  const nav = document.querySelector('.nav-links');
  nav.classList.toggle('open');
}

// ============================================
//  BOND DATA (simulates backend API response)
// ============================================
const BONDS_DATA = [
  { id:1, issuer:'Govt. of India 2034', type:'G-Sec', rating:'Sovereign', yield:7.18, maturity:'Mar 2034', minInvest:10000, isin:'IN0020190104', exchange:'BSE/NSE' },
  { id:2, issuer:'HDFC Bank Ltd.', type:'Corporate', rating:'AAA', yield:9.25, maturity:'Jun 2027', minInvest:10000, isin:'INE040A08378', exchange:'BSE' },
  { id:3, issuer:'NTPC Limited', type:'PSU', rating:'AAA', yield:8.75, maturity:'Jan 2029', minInvest:10000, isin:'INE733E07379', exchange:'NSE' },
  { id:4, issuer:'Tata Capital Financial Services', type:'Corporate', rating:'AA+', yield:10.50, maturity:'Sep 2026', minInvest:10000, isin:'INE306N07278', exchange:'BSE' },
  { id:5, issuer:'REC Limited', type:'PSU', rating:'AAA', yield:7.90, maturity:'Dec 2026', minInvest:10000, isin:'INE020B08BF5', exchange:'NSE' },
  { id:6, issuer:'Bajaj Finance Ltd.', type:'Corporate', rating:'AA+', yield:10.10, maturity:'Aug 2027', minInvest:10000, isin:'INE296A07PS5', exchange:'BSE' },
  { id:7, issuer:'State Govt. Maharashtra SDL', type:'G-Sec', rating:'Sovereign', yield:7.45, maturity:'Feb 2032', minInvest:10000, isin:'IN2320220209', exchange:'NSE' },
  { id:8, issuer:'Power Finance Corporation', type:'PSU', rating:'AAA', yield:8.30, maturity:'Nov 2030', minInvest:10000, isin:'INE134E08KQ4', exchange:'BSE/NSE' },
  { id:9, issuer:'Muthoot Finance Ltd.', type:'Corporate', rating:'AA', yield:11.50, maturity:'Mar 2026', minInvest:10000, isin:'INE414G07HK2', exchange:'BSE' },
  { id:10, issuer:'NHAI Bonds (54EC)', type:'54EC', rating:'Sovereign', yield:5.25, maturity:'Mar 2028', minInvest:10000, isin:'INE906B07GA6', exchange:'BSE' },
  { id:11, issuer:'Indian Railway Finance Corp.', type:'PSU', rating:'AAA', yield:7.68, maturity:'Jul 2031', minInvest:10000, isin:'INE053F07AZ3', exchange:'NSE' },
  { id:12, issuer:'L&T Finance Holdings', type:'Corporate', rating:'AA', yield:9.85, maturity:'Oct 2026', minInvest:10000, isin:'INE476M07244', exchange:'BSE' },
  { id:13, issuer:'Sovereign Gold Bond 2025-26 Series III', type:'SGB', rating:'Sovereign', yield:2.50, maturity:'Oct 2033', minInvest:4800, isin:'IN0020230034', exchange:'BSE/NSE' },
  { id:14, issuer:'Shriram Finance Ltd.', type:'Corporate', rating:'AA+', yield:10.75, maturity:'Apr 2027', minInvest:10000, isin:'INE721A07RH7', exchange:'BSE' },
  { id:15, issuer:'Govt. of India 2053 (30Y)', type:'G-Sec', rating:'Sovereign', yield:7.32, maturity:'Jun 2053', minInvest:10000, isin:'IN0020220139', exchange:'NSE' },
];

window.BONDS_DATA = BONDS_DATA;
