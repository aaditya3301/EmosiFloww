// Simple JWT for wallet address storage
export function createSimpleJWT(walletAddress: string): string {
  const header = { alg: "HS256", typ: "JWT" };
  const payload = { 
    walletAddress, 
    iat: Math.floor(Date.now() / 1000),
    exp: Math.floor(Date.now() / 1000) + (24 * 60 * 60) // 24 hours
  };
  
  const headerB64 = btoa(JSON.stringify(header));
  const payloadB64 = btoa(JSON.stringify(payload));
  
  // Simple signature (not cryptographically secure, just for demo)
  const signature = btoa(`${headerB64}.${payloadB64}.simple-secret`);
  
  return `${headerB64}.${payloadB64}.${signature}`;
}

export function decodeJWT(token: string): { walletAddress: string } | null {
  try {
    const parts = token.split('.');
    if (parts.length !== 3) return null;
    
    const payload = JSON.parse(atob(parts[1]));
    
    // Check expiration
    if (payload.exp && payload.exp < Math.floor(Date.now() / 1000)) {
      return null;
    }
    
    return { walletAddress: payload.walletAddress };
  } catch {
    return null;
  }
}