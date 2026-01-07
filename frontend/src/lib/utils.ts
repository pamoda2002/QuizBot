/**
 * Utility functions
 */

/**
 * Format a date string to a readable format
 */
export function formatDate(dateString: string): string {
  const date = new Date(dateString);
  
  // Format as HH:MM AM/PM
  const hours = date.getHours();
  const minutes = date.getMinutes();
  const ampm = hours >= 12 ? 'PM' : 'AM';
  const displayHours = hours % 12 || 12;
  const displayMinutes = minutes < 10 ? `0${minutes}` : minutes;
  
  return `${displayHours}:${displayMinutes} ${ampm}`;
}

/**
 * Generate a simple user ID (for demo purposes)
 * In production, this would come from authentication
 */
export function getUserId(): string {
  // Check if running in browser (not server-side)
  if (typeof window === 'undefined') {
    return 'user_temp';
  }
  
  let userId = localStorage.getItem('user_id');
  if (!userId) {
    userId = `user_${Math.random().toString(36).substr(2, 9)}`;
    localStorage.setItem('user_id', userId);
  }
  return userId;
}

/**
 * Truncate text to a specified length
 */
export function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) {
    return text;
  }
  return text.substring(0, maxLength) + '...';
}
