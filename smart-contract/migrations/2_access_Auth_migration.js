const accessAuth = artifacts.require("accessAuth");

module.exports = function (deployer) {
  deployer.deploy(accessAuth);
};
