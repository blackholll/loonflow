export const setCookie = (name: string, value: string, options: any = {}) => {
    options = {
      path: '/',
      ...options,
    };
  
    if (options.expires instanceof Date) {
      options.expires = options.expires.toUTCString();
    }
  
    let updatedCookie = `${name}=${value}`;
  
    for (let optionKey in options) {
      if (options.hasOwnProperty(optionKey)) { 
        const optionValue = options[optionKey];
        if (optionValue !== undefined && optionValue !== '') {
          updatedCookie += `; ${optionKey}`;
          if (optionValue !== true) {
            updatedCookie += `=${optionValue}`;
          }
        }
      }
    }
  
    document.cookie = updatedCookie;
  };
  
  export const getCookie = (name: string): string | undefined => {
    const matches = document.cookie.match(new RegExp(`(?:^|; )${name.replace(/([.$?*|{}()[\]\\/+^])/g, '\\$1')}=([^;]*)`));
    return matches ? decodeURIComponent(matches[1]) : undefined;
  };
  
  export const removeCookie = (name: string, options: any = {}) => {
    setCookie(name, '', {
      expires: -1,
      ...options,
    });
  };