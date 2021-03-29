# VVET

// **Please note this is a draft and this code is under heavy development. NOT to be used in production.**

## Credits

[WETH9](https://github.com/gnosis/canonical-weth/commit/0dd1ea3e295eef916d0c6223ec63141137d22d67)

## Disclaimer
Redistributions of source code must retain this list of conditions and the following disclaimer.

Neither the name of VeChain (VeChain Foundation) nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


## Problems:
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

## For Developers
```bash
make install # Install depedencies
make compile # Compile contracts
```