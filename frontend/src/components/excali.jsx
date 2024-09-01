const ExcaliComponent = () => {
  return React.createElement(
    React.Fragment,
    null,
    React.createElement(
      'div',
      {
        style: { height: '500px' },
      },
      React.createElement(ExcalidrawLib.Excalidraw),
    ),
  );
};

export default ExcaliComponent;
