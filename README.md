# VVET

## Instances on VeChain
|                                              Network                                               |                  Address                   |
| -------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| [mainnet](https://explore.vechain.org/accounts/0x0edab4e7e7d2c23d043f1352b7b10d899415ada7/)        | 0x0eDAb4E7e7D2c23D043f1352b7B10d899415ADA7 |
| [testnet](https://explore-testnet.vechain.org/accounts/0x535b9a56c2f03a3658fc8787c44087574eb381fd) | 0x535B9a56C2f03a3658FC8787C44087574eb381Fd |

## Credits

[WETH9](https://github.com/gnosis/canonical-weth/commit/0dd1ea3e295eef916d0c6223ec63141137d22d67)

## Disclaimer
Redistributions of source code must retain this list of conditions and the following disclaimer.

Neither the name of VeChain (VeChain Foundation) nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


## Problems & Solutions
```
// invalid opcode 0x47
// A new opcode, SELFBALANCE is introduced at 0x47

// https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1884.md

function totalSupply() public view returns (uint) {
        return address(this).balance;
}

// Fixed by:
Downgrade emv_verion from `Istanbul` to `Constantinople`
```

## Local Development
```bash
make install # Install depedencies
make compile # Compile contracts
```