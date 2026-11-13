/* Keep what makes these icons usable: the viewBox, the <title>, and the gradient ids. */
export default {
  multipass: true,
  js2svg: { pretty: true, indent: 2 },
  plugins: [
    {
      name: 'preset-default',
      params: {
        overrides: {
          removeViewBox: false,
          removeTitle: false,
          cleanupIds: false,
          convertShapeToPath: false,
        },
      },
    },
  ],
};
