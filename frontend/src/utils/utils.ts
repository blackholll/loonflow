import { parse } from 'querystring';

export const getPageQuery = () => {
    const { href } = window.location;
    const qsIndex = href.indexOf('?');
    const sharpIndex = href.indexOf('#');

    if (qsIndex !== -1) {
        if (qsIndex > sharpIndex) {
            return parse(href.split('?')[1]);
        }

        return parse(href.slice(qsIndex + 1, sharpIndex));
    }

    return {};
};

export const getCookie = (name: string) => {
    var strcookie = document.cookie;
    var arrcookie = strcookie.split("; ");
    for (var i = 0; i < arrcookie.length; i++) {
        var arr = arrcookie[i].split("=");
        if (arr[0] == name) {
            return arr[1];
        }
    }
    return "";
}

export const decodeJwt = (token: string) => decodeURIComponent(atob(token.split('.')[1].replace('-', '+').replace('_', '/')).split('').map(c => `%${('00' + c.charCodeAt(0).toString(16)).slice(-2)}`).join(''));
