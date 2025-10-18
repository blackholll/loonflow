import i18n from '../../../../i18n';

/**
 * Get translated validation message
 * @param key The translation key
 * @param params Optional parameters for interpolation
 * @returns Translated message
 */
export const t = (key: string, params?: Record<string, any>): string => {
  return i18n.t(key, params) as string;
};

/**
 * Get translated validation message for workflow validation
 * @param category The validation category (basic, connectivity, etc.)
 * @param messageKey The specific message key
 * @param params Optional parameters for interpolation
 * @returns Translated message
 */
export const getValidationMessage = (
  category: string,
  messageKey: string,
  params?: Record<string, any>
): string => {
  return t(`workflowValidation.${category}.${messageKey}`, params);
};
